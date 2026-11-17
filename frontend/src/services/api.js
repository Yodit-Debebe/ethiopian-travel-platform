const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
).replace(/\/+$/, '')

export async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('authToken')

  const isFormData = options.body instanceof FormData

  const headers = {
    ...options.headers,
  }

  // Let the browser set the multipart boundary for image uploads.
  if (!isFormData) {
    headers['Content-Type'] = 'application/json'
  }

  if (token) {
    headers.Authorization = `Token ${token}`
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
    signal: options.signal,
  })

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.error ||
      Object.values(data).flat().join(' ') ||
      'Something went wrong.'
    )
  }

  return data
}
