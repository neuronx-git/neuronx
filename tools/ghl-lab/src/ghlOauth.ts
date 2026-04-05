export type GhlOauthTokenResponse = {
  access_token: string
  token_type?: string
  expires_in?: number
  refresh_token?: string
  scope?: string
  locationId?: string
  companyId?: string
  userId?: string
  [k: string]: unknown
}

export function buildInstallUrl(params: {
  authUrl: string
  clientId: string
  redirectUri: string
  scope: string
  state: string
}): string {
  const url = new URL(params.authUrl)
  url.searchParams.set('response_type', 'code')
  url.searchParams.set('client_id', params.clientId)
  url.searchParams.set('redirect_uri', params.redirectUri)
  url.searchParams.set('scope', params.scope)
  url.searchParams.set('state', params.state)
  return url.toString()
}

export async function exchangeAuthorizationCode(params: {
  tokenUrl: string
  clientId: string
  clientSecret: string
  redirectUri: string
  code: string
}): Promise<GhlOauthTokenResponse> {
  const body = new URLSearchParams()
  body.set('grant_type', 'authorization_code')
  body.set('client_id', params.clientId)
  body.set('client_secret', params.clientSecret)
  body.set('redirect_uri', params.redirectUri)
  body.set('code', params.code)

  const res = await fetch(params.tokenUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body,
  })

  const text = await res.text()
  let json: any
  try {
    json = text ? JSON.parse(text) : {}
  } catch {
    json = { raw: text }
  }

  if (!res.ok) {
    const msg = typeof json?.error_description === 'string' ? json.error_description : typeof json?.message === 'string' ? json.message : `HTTP ${res.status}`
    throw new Error(`Token exchange failed: ${msg}`)
  }

  return json as GhlOauthTokenResponse
}

