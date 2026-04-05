import { execFile, spawn } from 'node:child_process'
import { promisify } from 'node:util'

const execFileAsync = promisify(execFile)

export async function readKeychainSecret(params: {
  service: string
  account: string
}): Promise<string> {
  const { stdout } = await execFileAsync(
    '/usr/bin/security',
    ['find-generic-password', '-w', '-s', params.service, '-a', params.account],
    { timeout: 10_000 },
  )
  const secret = stdout.trim()
  if (!secret) throw new Error('Empty secret returned from Keychain.')
  return secret
}

export async function writeKeychainSecret(params: {
  service: string
  account: string
  secret: string
}): Promise<void> {
  await new Promise<void>((resolve, reject) => {
    const child = spawn(
      '/usr/bin/security',
      ['add-generic-password', '-U', '-s', params.service, '-a', params.account, '-T', '', '-w'],
      { stdio: ['pipe', 'ignore', 'ignore'] },
    )

    child.once('error', reject)
    child.once('exit', (code) => {
      if (code === 0) resolve()
      else reject(new Error(`security add-generic-password exited with code ${code}`))
    })

    child.stdin.write(params.secret)
    child.stdin.write('\n')
    child.stdin.end()
  })
}

export function keychainWriteCommand(params: {
  service: string
  account: string
}): string {
  return `security add-generic-password -U -s "${params.service}" -a "${params.account}" -T "" -w`
}
