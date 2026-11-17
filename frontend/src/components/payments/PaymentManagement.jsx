
import { useEffect, useState } from 'react'
import { apiRequest } from '../../services/api'

const API_BASE_URL = 'http://127.0.0.1:8000'

async function fetchAllPages(endpoint) {
  let nextEndpoint = endpoint
  let allResults = []

  while (nextEndpoint) {
    const data = await apiRequest(nextEndpoint)

    if (Array.isArray(data)) {
      allResults = [...allResults, ...data]
      break
    }

    allResults = [...allResults, ...(data.results || [])]

    if (data.next) {
  const nextUrl = new URL(data.next, API_BASE_URL)

  if (nextUrl.origin !== API_BASE_URL) {
    throw new Error('Unexpected pagination URL.')
  }

  nextEndpoint = `${nextUrl.pathname}${nextUrl.search}`
} else {
  nextEndpoint = null
}
  }

  return allResults
}

function PaymentManagement({ onBack }) {
  const [bookings, setBookings] = useState([])
  const [payments, setPayments] = useState([])
  const [destinations, setDestinations] = useState({})
  const [paymentMethods, setPaymentMethods] = useState({})

  const [loading, setLoading] = useState(true)
  const [processingId, setProcessingId] = useState(null)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  useEffect(() => {
    async function loadPaymentData() {
      try {
        setLoading(true)
        setError('')

        const [
          bookingData,
          paymentData,
          destinationData,
        ] = await Promise.all([
          fetchAllPages('/api/bookings/'),
          fetchAllPages('/api/payments/'),
          fetchAllPages('/api/destinations/'),
        ])

        const destinationMap = {}

        destinationData.forEach((destination) => {
          destinationMap[destination.id] = destination
        })

        setBookings(bookingData)
        setPayments(paymentData)
        setDestinations(destinationMap)
      } catch (err) {
        setError(err.message || 'Unable to load payment information.')
      } finally {
        setLoading(false)
      }
    }

    loadPaymentData()
  }, [])

  const eligibleBookings = bookings.filter((booking) => {
    const hasActivePayment = payments.some(
      (payment) =>
        payment.booking === booking.id &&
        ['PENDING', 'SUCCESSFUL'].includes(payment.status)
    )

    return (
      booking.status === 'CONFIRMED' &&
      !hasActivePayment
    )
  })

  const handleCreatePayment = async (booking) => {
    setError('')
    setMessage('')
    setProcessingId(booking.id)

    try {
      const payment = await apiRequest('/api/payments/', {
        method: 'POST',
        body: JSON.stringify({
          booking: booking.id,
          payment_method:
            paymentMethods[booking.id] || 'TELEBIRR',
        }),
      })

      setPayments((previous) => [
        payment,
        ...previous,
      ])

      setMessage(
        `Payment #${payment.id} created successfully.`
      )
    } catch (err) {
      setError(err.message || 'Unable to create payment.')
    } finally {
      setProcessingId(null)
    }
  }

  const handleSimulatePayment = async (paymentId, result) => {
    setError('')
    setMessage('')
    setProcessingId(paymentId)

    try {
      const response = await apiRequest(
        `/api/payments/${paymentId}/simulate/`,
        {
          method: 'POST',
          body: JSON.stringify({ result }),
        }
      )

      setPayments((previous) =>
        previous.map((payment) =>
          payment.id === paymentId
            ? response.payment
            : payment
        )
      )

      setMessage(response.message)
    } catch (err) {
      setError(err.message || 'Unable to process payment.')
    } finally {
      setProcessingId(null)
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString(
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
      <section className="payments-page">
        <p>Loading payment information...</p>
      </section>
    )
  }

  return (
    <section className="payments-page">
      <button
        type="button"
        className="back-button"
        onClick={onBack}
      >
        ← Back to home
      </button>

      <div className="payments-heading">
        <span className="section-kicker">
          SECURE YOUR JOURNEY
        </span>

        <h1>My Payments</h1>

        <p>
          Manage payments for your confirmed travel bookings.
        </p>
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

      {/* Eligible bookings */}
      <div className="payment-section">
        <h2>Bookings awaiting payment</h2>

        {eligibleBookings.length === 0 ? (
          <div className="empty-payments">
            <h3>No bookings awaiting payment</h3>

            <p>
              You need a confirmed booking before creating a payment.
            </p>
          </div>
        ) : (
          <div className="payment-booking-list">
            {eligibleBookings.map((booking) => {
              const destination = destinations[booking.destination]

              return (
                <article
                  className="payment-booking-card"
                  key={booking.id}
                >
                  <div>
                    <span className="booking-reference">
                      Booking #{booking.id}
                    </span>

                    <h3>
                      {destination
                        ? destination.name
                        : `Destination #${booking.destination}`}
                    </h3>

                    <p>
                      Travel date: {formatDate(booking.travel_date)}
                    </p>

                    <p>
                      Travelers: {booking.number_of_travelers}
                    </p>

                    <h4>
                      {Number(
                        booking.total_price
                      ).toLocaleString()} ETB
                    </h4>
                  </div>

                  <div className="payment-booking-actions">
                    <label htmlFor={`method-${booking.id}`}>
                      Payment method
                    </label>

                    <select
                      id={`method-${booking.id}`}
                      value={
                        paymentMethods[booking.id] || 'TELEBIRR'
                      }
                      onChange={(event) =>
                        setPaymentMethods((previous) => ({
                          ...previous,
                          [booking.id]: event.target.value,
                        }))
                      }
                    >
                      <option value="TELEBIRR">
                        Telebirr
                      </option>

                      <option value="CBE_BIRR">
                        CBE Birr
                      </option>

                      <option value="BANK_TRANSFER">
                        Bank Transfer
                      </option>
                    </select>

                    <button
                      type="button"
                      className="create-payment-button"
                      disabled={processingId === booking.id}
                      onClick={() => handleCreatePayment(booking)}
                    >
                      {processingId === booking.id
                        ? 'Creating...'
                        : 'Create payment'}
                    </button>
                  </div>
                </article>
              )
            })}
          </div>
        )}
      </div>

      {/* Payment history */}
      <div className="payment-section">
        <h2>Payment history</h2>

        {payments.length === 0 ? (
          <div className="empty-payments">
            <p>You haven't created any payments yet.</p>
          </div>
        ) : (
          <div className="payment-history-list">
            {payments.map((payment) => {
              const booking = bookings.find(
                (item) => item.id === payment.booking
              )

              const destination = booking
                ? destinations[booking.destination]
                : null

              return (
                <article
                  className="payment-history-card"
                  key={payment.id}
                >
                  <div className="payment-history-header">
                    <div>
                      <span className="booking-reference">
                        Payment #{payment.id}
                      </span>

                      <h3>
                        {destination
                          ? destination.name
                          : `Booking #${payment.booking}`}
                      </h3>
                    </div>

                    <span
                      className={`payment-status payment-${payment.status.toLowerCase()}`}
                    >
                      {payment.status}
                    </span>
                  </div>

                  <div className="payment-history-details">
                    <p>
                      <strong>Amount:</strong>{' '}
                      {Number(payment.amount).toLocaleString()} ETB
                    </p>

                    <p>
                      <strong>Method:</strong>{' '}
                      {payment.payment_method.replaceAll('_', ' ')}
                    </p>

                    <p>
                      <strong>Transaction reference:</strong>
                    </p>

                    <code className="transaction-reference">
                      {payment.transaction_reference}
                    </code>

                    <p>
                      <strong>Created:</strong>{' '}
                      {formatDate(payment.created_at)}
                    </p>
                  </div>

                  {payment.status === 'PENDING' && (
                    <div className="simulation-actions">
                      <p>
                        Demo payment simulation — no real money
                        will be transferred.
                      </p>

                      <button
                        type="button"
                        className="simulate-success-button"
                        disabled={processingId === payment.id}
                        onClick={() =>
                          handleSimulatePayment(
                            payment.id,
                            'SUCCESSFUL'
                          )
                        }
                      >
                        Simulate success
                      </button>

                      <button
                        type="button"
                        className="simulate-failure-button"
                        disabled={processingId === payment.id}
                        onClick={() =>
                          handleSimulatePayment(
                            payment.id,
                            'FAILED'
                          )
                        }
                      >
                        Simulate failure
                      </button>
                    </div>
                  )}
                </article>
              )
            })}
          </div>
        )}
      </div>
    </section>
  )
}

export default PaymentManagement
