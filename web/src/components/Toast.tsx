import { useEffect } from 'react'

interface ToastProps {
  message: string
  onDismiss: () => void
  durationMs?: number
}

export default function Toast({ message, onDismiss, durationMs = 1500 }: ToastProps) {
  useEffect(() => {
    const timer = window.setTimeout(onDismiss, durationMs)
    return () => window.clearTimeout(timer)
  }, [message, durationMs, onDismiss])

  return (
    <div className="toast toast-success" role="status" aria-live="polite">
      {message}
    </div>
  )
}
