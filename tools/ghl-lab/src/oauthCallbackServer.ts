import http from 'node:http'
import { URL } from 'node:url'
import fs from 'node:fs'
import path from 'node:path'
import { buildInstallUrl, exchangeAuthorizationCode } from './ghlOauth'
import { readKeychainSecret } from './keychain'
import { GhlV2Client } from './ghlV2'

type StartServerParams = {
  authUrl: string
  tokenUrl: string
  redirectUri: string
  apiBaseUrl: string
  apiVersion: string
  goldLocationName: string
  scope: string
  state: string
  keychainService: string
  clientIdAccount: string
  clientSecretAccount: string
}

export async function startOauthCallbackServer(params: StartServerParams): Promise<{
  installUrl: string
  done: Promise<{ locationId: string; companyId?: string; userType?: string }>
  close: () => Promise<void>
}> {
  const clientId = await readKeychainSecret({ service: params.keychainService, account: params.clientIdAccount }).catch(() => {
    throw new Error(
      `Missing OAuth Client ID in Keychain. Store it using:\n\n${keychainWriteCommand({ service: params.keychainService, account: params.clientIdAccount })}\n`,
    )
  })

  const clientSecret = await readKeychainSecret({ service: params.keychainService, account: params.clientSecretAccount }).catch(() => {
    throw new Error(
      `Missing OAuth Client Secret in Keychain. Store it using:\n\n${keychainWriteCommand({ service: params.keychainService, account: params.clientSecretAccount })}\n`,
    )
  })

  const redirect = new URL(params.redirectUri)
  const hostname = redirect.hostname
  const port = Number(redirect.port || (redirect.protocol === 'https:' ? 443 : 80))
  const pathname = redirect.pathname

  if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
    throw new Error(
      `Redirect URI must point to localhost for this local callback server. Current: ${params.redirectUri}\n` +
        `Either update the Marketplace app redirect URI to localhost for lab, or deploy a hosted callback endpoint.`,
    )
  }

  const installUrl = buildInstallUrl({
    authUrl: params.authUrl,
    clientId,
    redirectUri: params.redirectUri,
    scope: params.scope,
    state: params.state,
  })

  let resolveDone: ((value: { locationId: string; companyId?: string; userType?: string }) => void) | undefined
  let rejectDone: ((err: unknown) => void) | undefined
  const done = new Promise<{ locationId: string; companyId?: string; userType?: string }>((resolve, reject) => {
    resolveDone = resolve
    rejectDone = reject
  })

  const server = http.createServer(async (req, res) => {
    try {
      const reqUrl = new URL(req.url ?? '/', `http://localhost:${port}`)
      if (reqUrl.pathname !== pathname) {
        res.writeHead(404, { 'Content-Type': 'text/plain' })
        res.end('Not Found')
        return
      }

      const code = reqUrl.searchParams.get('code')
      const state = reqUrl.searchParams.get('state')
      const locationIdFromQuery =
        reqUrl.searchParams.get('locationId') ??
        reqUrl.searchParams.get('location_id') ??
        reqUrl.searchParams.get('location')

      if (!code) {
        res.writeHead(400, { 'Content-Type': 'text/plain' })
        res.end('Missing code')
        return
      }
      if (state && state !== params.state) {
        res.writeHead(400, { 'Content-Type': 'text/plain' })
        res.end('Invalid state')
        return
      }

      const token = await exchangeAuthorizationCode({
        tokenUrl: params.tokenUrl,
        clientId,
        clientSecret,
        redirectUri: params.redirectUri,
        code,
      })

      const accessToken = typeof (token as any).access_token === 'string' ? ((token as any).access_token as string) : undefined
      const refreshToken = typeof (token as any).refresh_token === 'string' ? ((token as any).refresh_token as string) : undefined

      if (!accessToken || !refreshToken) {
        res.writeHead(500, { 'Content-Type': 'text/plain' })
        res.end('Token response missing access_token or refresh_token')
        rejectDone?.(new Error('Token response missing access_token or refresh_token'))
        return
      }

      const companyId = typeof (token as any).companyId === 'string' ? ((token as any).companyId as string) : undefined
      const userType = typeof (token as any).userType === 'string' ? ((token as any).userType as string) : undefined

      const tokenLocationId =
        typeof (token as any).locationId === 'string'
          ? ((token as any).locationId as string)
          : typeof (token as any).location_id === 'string'
            ? ((token as any).location_id as string)
            : undefined

      let locationId = locationIdFromQuery ?? tokenLocationId

      const v2 = new GhlV2Client({ baseUrl: params.apiBaseUrl, token: accessToken, version: params.apiVersion })

      if (!locationId && userType === 'Company' && companyId) {
        let skip = 0
        const limit = 100
        let found: string | undefined
        for (let page = 0; page < 25; page++) {
          const data = await v2.searchLocations({ companyId, skip, limit })
          const locations = Array.isArray((data as any).locations) ? ((data as any).locations as any[]) : []
          for (const loc of locations) {
            if (typeof loc?.name === 'string' && loc.name.trim().toLowerCase() === params.goldLocationName.trim().toLowerCase()) {
              if (typeof loc?.id === 'string') found = loc.id
            }
          }
          if (found) break
          if (locations.length < limit) break
          skip += limit
        }

        if (found) {
          const locToken = await v2.getLocationTokenFromAgency({ companyId, locationId: found })
          const locId = typeof locToken?.locationId === 'string' ? (locToken.locationId as string) : found
          if (locId) locationId = locId
        }
      }

      void refreshToken
      if (!locationId) {
        const keys = Object.keys(token ?? {}).filter(
          (k) => !['access_token', 'refresh_token', 'id_token'].includes(k),
        )
        res.writeHead(500, { 'Content-Type': 'text/plain' })
        res.end(
          `Token response missing locationId. Non-sensitive keys present: ${keys.join(', ')}\n` +
            `If your app Target User is Agency, this is expected. Create a sub-account named "NeuronX Test Lab" and rerun install, or provide the locationId.`,
        )
        rejectDone?.(new Error('Token response missing locationId'))
        return
      }

      res.writeHead(200, { 'Content-Type': 'text/html' })
      res.end(
        `<html><body><h2>NeuronX OAuth Connected</h2><p>Location: ${locationId}</p><p>You can close this window.</p></body></html>`,
      )

      process.stdout.write(`\nOAUTH_OK locationId=${locationId}${companyId ? ` companyId=${companyId}` : ''}${userType ? ` userType=${userType}` : ''}\n`)

      resolveDone?.({ locationId, companyId, userType })

      const tokenStorePath = path.resolve(process.cwd(), '.tokens.json')
      try {
        const payload = {
          access_token: accessToken,
          refresh_token: refreshToken,
          location_id: locationId,
          company_id: companyId ?? null,
          user_type: userType ?? null,
          stored_at: new Date().toISOString(),
        }
        fs.writeFileSync(tokenStorePath, JSON.stringify(payload, null, 2), 'utf-8')
        process.stdout.write(`Tokens written to ${tokenStorePath}\n`)
      } catch (e) {
        process.stdout.write(`Token file write failed: ${e instanceof Error ? e.message : e}\n`)
      }

      setTimeout(() => {
        server.close()
      }, 250)
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'text/plain' })
      res.end('OAuth callback failed')
      const msg = e instanceof Error ? e.message : String(e)
      process.stdout.write(`OAuth callback failed: ${msg}\n`)
      rejectDone?.(new Error(`OAuth callback failed: ${msg}`))
    }
  })

  await new Promise<void>((resolve, reject) => {
    server.once('error', reject)
    server.listen(port, '127.0.0.1', () => resolve())
  })

  return {
    installUrl,
    done,
    close: async () => {
      await new Promise<void>((resolve) => server.close(() => resolve()))
    },
  }
}
