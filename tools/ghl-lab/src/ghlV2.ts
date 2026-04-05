export type GhlLocation = {
  id: string
  name?: string
  companyId?: string
  [k: string]: unknown
}

export class GhlV2Client {
  constructor(
    private readonly opts: {
      baseUrl: string
      token: string
      version: string
    },
  ) {}

  private async request(path: string, init: RequestInit): Promise<any> {
    const url = new URL(path, this.opts.baseUrl)
    const res = await fetch(url.toString(), {
      ...init,
      headers: {
        Accept: 'application/json',
        Version: this.opts.version,
        Authorization: `Bearer ${this.opts.token}`,
        ...(init.headers ?? {}),
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
      throw new Error(`GHL v2 request failed: ${msg}`)
    }
    return json
  }

  async searchLocations(params: {
    companyId: string
    skip?: number
    limit?: number
  }): Promise<{ locations: GhlLocation[] } | any> {
    const url = new URL('/locations/search', this.opts.baseUrl)
    url.searchParams.set('companyId', params.companyId)
    url.searchParams.set('skip', String(params.skip ?? 0))
    url.searchParams.set('limit', String(params.limit ?? 100))
    return this.request(url.pathname + url.search, { method: 'GET' })
  }

  async getLocationTokenFromAgency(params: {
    companyId: string
    locationId: string
  }): Promise<any> {
    const body = new URLSearchParams()
    body.set('companyId', params.companyId)
    body.set('locationId', params.locationId)

    return this.request('/oauth/locationToken', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body,
    })
  }
}

