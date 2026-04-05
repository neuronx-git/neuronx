import { GhlV1Client } from './ghlV1'

export type KeyTypeGuess =
  | { type: 'agency_api_key'; confidence: 'high' | 'medium'; reason: string }
  | { type: 'not_agency_api_key'; confidence: 'high' | 'medium'; reason: string }

function looksLikeAgencyApiKey(key: string): boolean {
  return /^[a-f0-9]{24}-[a-z0-9]+$/i.test(key)
}

export async function guessKeyType(params: {
  baseUrl: string
  key: string
}): Promise<KeyTypeGuess> {
  if (looksLikeAgencyApiKey(params.key)) {
    return {
      type: 'agency_api_key',
      confidence: 'medium',
      reason: 'Matches common HighLevel agency API key format (<24-hex>-<suffix>).',
    }
  }

  const client = new GhlV1Client({ baseUrl: params.baseUrl, agencyApiKey: params.key })

  try {
    await client.listLocations()
    return {
      type: 'agency_api_key',
      confidence: 'high',
      reason: 'Successfully called v1 /locations list endpoint.',
    }
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e)
    if (msg.toLowerCase().includes('unauthorized') || msg.toLowerCase().includes('forbidden')) {
      return {
        type: 'not_agency_api_key',
        confidence: 'high',
        reason: 'Authorization failed against v1 /locations list endpoint.',
      }
    }
    return {
      type: 'not_agency_api_key',
      confidence: 'medium',
      reason: `Could not validate key against v1 /locations list endpoint: ${msg}`,
    }
  }
}
