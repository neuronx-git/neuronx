import { execFile } from 'node:child_process'
import { promisify } from 'node:util'

const execFileAsync = promisify(execFile)

export async function getAgencyApiKey(params: {
  envKey?: string
  keychainService: string
  keychainAccount: string
}): Promise<string> {
  if (params.envKey && params.envKey.trim().length > 0) {
    return params.envKey.trim()
  }

  try {
    const { stdout } = await execFileAsync(
      '/usr/bin/security',
      ['find-generic-password', '-w', '-s', params.keychainService, '-a', params.keychainAccount],
      {
        timeout: 10_000,
      },
    )

    const key = stdout.trim()
    if (!key) {
      throw new Error('Empty key returned from Keychain.')
    }
    return key
  } catch {
    throw new Error(
      `Missing agency API key. Set GHL_AGENCY_API_KEY in the process env, or store it in macOS Keychain using:\n\n` +
        `security add-generic-password -U -s "${params.keychainService}" -a "${params.keychainAccount}" -T "" -w\n\n` +
        `Then rerun the command. This prompts for the secret without echoing it.`,
    )
  }
}

