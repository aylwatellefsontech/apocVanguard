export function errorMessage(err: unknown): string {
  return err instanceof Error ? err.message : 'Unknown error'
}

export function isENOENT(err: unknown): boolean {
  return (
    typeof err === 'object' &&
    err !== null &&
    'code' in err &&
    (err as NodeJS.ErrnoException).code === 'ENOENT'
  )
}
