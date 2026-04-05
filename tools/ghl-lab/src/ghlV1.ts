export type GhlV1CreateLocationInput = {
  businessName: string
  address?: string
  city?: string
  country?: string
  state?: string
  postalCode?: string
  website?: string
  timezone?: string
  firstName?: string
  lastName?: string
  email?: string
  phone?: string
  settings?: {
    allowDuplicateContact?: boolean
    allowDuplicateOpportunity?: boolean
    allowFacebookNameMerge?: boolean
    disableContactTimezone?: boolean
  }
  snapshot?: {
    id: string
    type?: string
  }
}

export type GhlV1CreateLocationResponse = {
  id?: string
  locationId?: string
  companyId?: string
  message?: string
  [k: string]: unknown
}

export class GhlV1Client {
  constructor(
    private readonly opts: {
      baseUrl: string
      agencyApiKey: string
    },
  ) {}

  async createLocation(input: GhlV1CreateLocationInput): Promise<GhlV1CreateLocationResponse> {
    const url = new URL('/v1/locations', this.opts.baseUrl)
    const res = await fetch(url.toString(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${this.opts.agencyApiKey}`,
      },
      body: JSON.stringify(input),
    })

    const text = await res.text()
    let json: any
    try {
      json = text ? JSON.parse(text) : {}
    } catch {
      json = { raw: text }
    }

    if (!res.ok) {
      const msg = typeof json?.message === 'string' ? json.message : `HTTP ${res.status}`
      throw new Error(`GHL v1 create location failed: ${msg}`)
    }

    return json as GhlV1CreateLocationResponse
  }

  async listLocations(): Promise<unknown> {
    const url = new URL('/v1/locations', this.opts.baseUrl)
    const res = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${this.opts.agencyApiKey}`,
      },
    })

    const text = await res.text()
    let json: any
    try {
      json = text ? JSON.parse(text) : {}
    } catch {
      json = { raw: text }
    }

    if (!res.ok) {
      const msg = typeof json?.message === 'string' ? json.message : `HTTP ${res.status}`
      throw new Error(`GHL v1 list locations failed: ${msg}`)
    }

    return json
  }
}
