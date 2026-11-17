import { useEffect, useState } from 'react'
import { apiRequest } from '../../services/api'

const API_BASE_URL = 'http://127.0.0.1:8000'

async function fetchAllPages(endpoint) {
  let nextEndpoint = endpoint
  let allResults = []

  while (nextEndpoint) {
    const data = await apiRequest(nextEndpoint)

    if (Array.isArray(data)) {
      allResults.push(...data)
      break
    }

    allResults.push(...(data.results || []))

    if (data.next) {
      const nextUrl = new URL(data.next, API_BASE_URL)
      const apiBaseUrl = new URL(API_BASE_URL)

      if (nextUrl.origin !== apiBaseUrl.origin) {
        throw new Error('Unexpected pagination URL.')
      }

      nextEndpoint = `${nextUrl.pathname}${nextUrl.search}`
    } else {
      nextEndpoint = null
    }
  }

  return allResults
}

function MyBookings({ onBack }) {
  const [bookings, setBookings] = useState([])
  const [destinations, setDestinations] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [cancellingId, setCancellingId] = useState(null)
  const [message, setMessage] = useState('')

  useEffect(() => {
    let isActive = true

    async function loadInitialBookings() {
      try {
        const [bookingData, destinationData] = await Promise.all([
          fetchAllPages('/api/bookings/'),
          fetchAllPages('/api/destinations/'),
        ])

        if (!isActive) return

        const destinationMap = {}

        destinationData.forEach((destination) => {
          destinationMap[destination.id] = destination
        })

        setBookings(bookingData)
        setDestinations(destinationMap)
      } catch (err) {
        if (isActive) {
          setError(err.message || 'Unable to load your bookings.')
        }
      } finally {
        if (isActive) {
          setLoading(false)
        }
      }
    }

    loadInitialBookings()

    return () => {
      isActive = false
    }
  }, [])
  const handleCancel = async (bookingId) => {
    setError('')
    setMessage('')
    setCancellingId(bookingId)

    try {
      const response = await apiRequest(
        `/api/bookings/${bookingId}/cancel/`,
        {
          method: 'POST',
        }
      )

      setBookings((previousBookings) =>
        previousBookings.map((booking) =>
          booking.id === bookingId
            ? response.booking
            : booking
        )
      )

      setMessage(`Booking #${bookingId} was cancelled successfully.`)
    } catch (err) {
      setError(err.message || 'Unable to cancel this booking.')
    } finally {
      setCancellingId(null)
    }
  }

  const formatDate = (dateString) => {
    return new Date(`${dateString}T00:00:00`).toLocaleDateString(
      'en-US',
      {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      }
    )
  }

  if (loading) {
    return (
      <section className="my-bookings">
        <p>Loading your bookings...</p>
      </section>
    )
  }

  return (
    <section className="my-bookings">
      <button
        type="button"
        className="back-button"
        onClick={onBack}
      >
        ← Back to home
      </button>

      <div className="my-bookings-heading">
        <h1>My Bookings</h1>
        <p>View and manage your travel bookings.</p>
      </div>

      {error && (
        <div className="auth-error">
          {error}
        </div>
      )}

      {message && (
        <div className="booking-message">
          {message}
        </div>
      )}

      {bookings.length === 0 ? (
        <div className="empty-bookings">
          <h3>No bookings yet</h3>
          <p>
            You haven't made any travel bookings.
            Explore our destinations and plan your next trip!
          </p>
        </div>
      ) : (
        <div className="booking-list">
          {bookings.map((booking) => {
            const destination = destinations[booking.destination]

            return (
              <article
                className="booking-card"
                key={booking.id}
              >
                <div className="booking-card-header">
                  <div>
                    <span className="booking-reference">
                      Booking #{booking.id}
                    </span>

                    <h3>
                      {destination
                        ? destination.name
                        : `Destination #${booking.destination}`}
                    </h3>
                  </div>

                  <span
                    className={`booking-status status-${booking.status.toLowerCase()}`}
                  >
                    {booking.status}
                  </span>
                </div>

                <div className="booking-card-details">
                  <p>
                    <strong>Travel date:</strong>{' '}
                    {formatDate(booking.travel_date)}
                  </p>

                  <p>
                    <strong>Travelers:</strong>{' '}
                    {booking.number_of_travelers}
                  </p>

                  <p>
                    <strong>Total price:</strong>{' '}
                    {Number(booking.total_price).toLocaleString()} ETB
                  </p>

                  <p>
                    <strong>Booked on:</strong>{' '}
                    {new Date(booking.created_at).toLocaleDateString()}
                  </p>
                </div>

                {booking.status === 'PENDING' && (
                  <button
                    type="button"
                    className="cancel-booking-button"
                    onClick={() => handleCancel(booking.id)}
                    disabled={cancellingId === booking.id}
                  >
                    {cancellingId === booking.id
                      ? 'Cancelling...'
                      : 'Cancel booking'}
                  </button>
                )}
              </article>
            )
          })}
        </div>
      )}
    </section>
  )
}

export default MyBookings
