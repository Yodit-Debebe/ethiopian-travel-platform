import { useEffect, useState } from 'react'
import { apiRequest } from '../services/api'

const API_BASE_URL = 'http://127.0.0.1:8000'

function useDestinations() {
  const [destinations, setDestinations] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const controller = new AbortController()

    async function fetchDestinations() {
      try {
        setLoading(true)
        setError('')

        let nextUrl = '/api/destinations/'
        const allDestinations = []

        while (nextUrl) {
          const url = new URL(nextUrl, API_BASE_URL)
          const apiBaseUrl = new URL(API_BASE_URL)

          if (url.origin !== apiBaseUrl.origin) {
            throw new Error('Unexpected pagination URL.')
          }

          const endpoint = `${url.pathname}${url.search}`

          const data = await apiRequest(endpoint, {
            signal: controller.signal,
          })

          allDestinations.push(...(data.results || []))
          nextUrl = data.next
        }

        setDestinations(allDestinations)
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error('Failed to fetch destinations:', err)
          setError('Unable to load destinations. Please try again.')
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false)
        }
      }
    }

    fetchDestinations()

    return () => controller.abort()
  }, [])

  return {
    destinations,
    setDestinations,
    loading,
    error,
    setError,
  }
}

export default useDestinations