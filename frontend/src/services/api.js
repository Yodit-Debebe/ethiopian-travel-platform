const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
).replace(/\/+$/, '')

async function sendRequest(endpoint, options, token) {
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

  return { response, data }
}

export async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('authToken')

  let { response, data } = await sendRequest(endpoint, options, token)

  // A stale or expired token must not block public endpoints. Clear the
  // session and retry anonymously so pages like the destination list load.
  if (response.status === 401 && token) {
    localStorage.removeItem('authToken')
    localStorage.removeItem('currentUser')
    window.dispatchEvent(new Event('auth:expired'))

    ;({ response, data } = await sendRequest(endpoint, options, null))
  }

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
