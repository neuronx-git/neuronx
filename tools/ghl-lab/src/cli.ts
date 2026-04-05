import { getEnv } from './env'
import { GhlV1Client } from './ghlV1'
import { guessKeyType } from './keyIntrospection'
import { getAgencyApiKey } from './secret'
import { startOauthCallbackServer } from './oauthCallbackServer'

type Args = {
  command?: string
  name?: string
  snapshotId?: string
}

function parseArgs(argv: string[]): Args {
  const args: Args = {}
  const [command, ...rest] = argv
  args.command = command

  for (let i = 0; i < rest.length; i++) {
    const token = rest[i]
    if (token === '--name') args.name = rest[++i]
    else if (token === '--snapshotId') args.snapshotId = rest[++i]
  }

  return args
}

function printUsage(): void {
  console.log(`Usage:
  pnpm ghl:lab identify-key
  pnpm ghl:lab create-location --name "NeuronX Test Lab" [--snapshotId <SNAPSHOT_ID>]
  pnpm ghl:lab oauth:server

Environment:
  GHL_AGENCY_API_KEY (optional if using Keychain)
  GHL_KEYCHAIN_SERVICE (optional, default: neuronx-ghl)
  GHL_KEYCHAIN_ACCOUNT (optional, default: agency-api-key)
  GHL_V1_BASE_URL (optional, default: https://rest.gohighlevel.com)
  GHL_DEFAULT_TIMEZONE (optional, default: Canada/Eastern)

OAuth (Marketplace) defaults:
  GHL_OAUTH_AUTH_URL (default: https://marketplace.gohighlevel.com/oauth/chooselocation)
  GHL_OAUTH_TOKEN_URL (default: https://services.leadconnectorhq.com/oauth/token)
  GHL_OAUTH_REDIRECT_URI (default: http://localhost:3000/integrations/ghl/auth/callback)
`)
}

async function main(): Promise<void> {
  const env = getEnv()
  const args = parseArgs(process.argv.slice(2))

  const needsAgencyKey = args.command === 'identify-key' || args.command === 'create-location'
  const agencyApiKey = needsAgencyKey
    ? await getAgencyApiKey({
        envKey: env.GHL_AGENCY_API_KEY,
        keychainService: env.GHL_KEYCHAIN_SERVICE,
        keychainAccount: env.GHL_KEYCHAIN_ACCOUNT,
      })
    : undefined

  if (!args.command) {
    printUsage()
    process.exit(1)
  }

  if (args.command === 'create-location') {
    if (!args.name) {
      throw new Error('Missing --name')
    }

    const client = new GhlV1Client({
      baseUrl: env.GHL_V1_BASE_URL,
      agencyApiKey: agencyApiKey!,
    })

    const payload: any = {
      businessName: args.name,
      address: '3500 Deer Creek Road',
      city: 'Palo Alto',
      country: 'US',
      state: 'CA',
      postalCode: '94304',
      website: 'https://example.com',
      timezone: env.GHL_DEFAULT_TIMEZONE,
      firstName: 'NeuronX',
      lastName: 'Admin',
      email: 'admin@example.com',
      phone: '+15555550123',
      settings: {
        allowDuplicateContact: false,
        allowDuplicateOpportunity: false,
        allowFacebookNameMerge: false,
        disableContactTimezone: false,
      },
    }

    if (args.snapshotId) {
      payload.snapshot = {
        id: args.snapshotId,
        type: 'vertical',
      }
    }

    const res = await client.createLocation(payload)
    const locationId = (res.locationId ?? res.id) as string | undefined
    if (!locationId) {
      console.log('Create location succeeded but no location id returned. Full response:')
      console.log(JSON.stringify(res, null, 2))
      return
    }

    console.log(`Created location: ${locationId}`)
    console.log(`Dashboard URL: https://app.gohighlevel.com/location/${locationId}`)
    return
  }

  if (args.command === 'identify-key') {
    const guess = await guessKeyType({
      baseUrl: env.GHL_V1_BASE_URL,
      key: agencyApiKey!,
    })
    console.log(`Key type guess: ${guess.type} (${guess.confidence})`)
    console.log(`Reason: ${guess.reason}`)
    return
  }

  if (args.command === 'oauth:server') {
    const { installUrl, done } = await startOauthCallbackServer({
      authUrl: env.GHL_OAUTH_AUTH_URL,
      tokenUrl: env.GHL_OAUTH_TOKEN_URL,
      redirectUri: env.GHL_OAUTH_REDIRECT_URI,
      apiBaseUrl: env.GHL_API_BASE_URL,
      apiVersion: env.GHL_API_VERSION,
      goldLocationName: env.GHL_GOLD_LOCATION_NAME,
      scope: env.GHL_OAUTH_SCOPE,
      state: 'neuronx_lab',
      keychainService: env.GHL_KEYCHAIN_SERVICE,
      clientIdAccount: 'oauth-client-id',
      clientSecretAccount: 'oauth-client-secret',
    })

    console.log(`Install URL (open in browser): ${installUrl}`)
    console.log(`Waiting for OAuth callback ...`)

    const result = await done
    console.log(
      `OAuth complete for locationId=${result.locationId}` +
        (result.companyId ? ` companyId=${result.companyId}` : '') +
        (result.userType ? ` userType=${result.userType}` : ''),
    )
    return
  }

  printUsage()
  process.exit(1)
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : err)
  process.exit(1)
})
