import { z } from 'zod'

const envSchema = z.object({
  GHL_AGENCY_API_KEY: z.string().min(1).optional(),
  GHL_KEYCHAIN_SERVICE: z.string().min(1).optional().default('neuronx-ghl'),
  GHL_KEYCHAIN_ACCOUNT: z.string().min(1).optional().default('agency-api-key'),
  GHL_V1_BASE_URL: z.string().url().optional().default('https://rest.gohighlevel.com'),
  GHL_DEFAULT_TIMEZONE: z.string().optional().default('Canada/Eastern'),

  GHL_OAUTH_AUTH_URL: z.string().url().optional().default('https://marketplace.gohighlevel.com/oauth/chooselocation'),
  GHL_OAUTH_TOKEN_URL: z
    .string()
    .url()
    .optional()
    .default('https://services.leadconnectorhq.com/oauth/token'),
  GHL_OAUTH_REDIRECT_URI: z.string().url().optional().default('http://localhost:3000/auth/neuronx/callback'),
  GHL_OAUTH_SCOPE: z
    .string()
    .min(1)
    .optional()
    .default(
      [
        'locations.readonly',
        'locations/customFields.readonly',
        'locations/customFields.write',
        'locations/customValues.readonly',
        'locations/customValues.write',
        'locations/tags.readonly',
        'locations/tags.write',
        'locations/tasks.readonly',
        'locations/tasks.write',
        'opportunities.readonly',
        'opportunities.write',
        'calendars.readonly',
        'calendars.write',
        'calendars/events.readonly',
        'calendars/events.write',
        'contacts.readonly',
        'contacts.write',
        'forms.readonly',
        'workflows.readonly',
        'oauth.readonly',
        'oauth.write',
        'emails/builder.readonly',
        'emails/builder.write',
      ].join(' '),
    ),

  GHL_API_BASE_URL: z.string().url().optional().default('https://services.leadconnectorhq.com'),
  GHL_API_VERSION: z.string().min(1).optional().default('2021-07-28'),
  GHL_GOLD_LOCATION_NAME: z.string().min(1).optional().default('NeuronX Test Lab'),
})

export type Env = z.infer<typeof envSchema>

export function getEnv(): Env {
  const parsed = envSchema.safeParse(process.env)
  if (!parsed.success) {
    const issues = parsed.error.issues.map((i) => `${i.path.join('.')}: ${i.message}`).join('\n')
    throw new Error(`Missing/invalid environment variables:\n${issues}`)
  }
  return parsed.data
}
