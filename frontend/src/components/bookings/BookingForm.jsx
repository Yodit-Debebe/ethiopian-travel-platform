
import { useState } from 'react'
import { apiRequest } from '../../services/api'

function getTodayDate() {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

function BookingForm({ destination, onBookingSuccess }) {
  const [travelDate, setTravelDate] = useState('')
  const [travelers, setTravelers] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(null)

  const totalPrice = Number(destination.price) * Number(travelers)

  const handleSubmit = async (event) => {
    event.preventDefault()

    setError('')
    setSuccess(null)

    if (!travelDate) {
      setError('Please select your travel date.')
      return
    }

    setLoading(true)

    try {
      const booking = await apiRequest('/api/bookings/', {
        method: 'POST',
        body: JSON.stringify({
          destination: destination.id,
          travel_date: travelDate,
          number_of_travelers: Number(travelers),
        }),
      })

      setSuccess(booking)
      setTravelDate('')
      setTravelers(1)

      if (onBookingSuccess) {
        onBookingSuccess(booking)
      }
    } catch (err) {
      setError(err.message || 'Unable to create your booking.')
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <div className="booking-success">
        <h3>Booking submitted successfully!</h3>
        <p>Your booking has been received.</p>

        <p>
          Booking reference: <strong>#{success.id}</strong>
        </p>

        <p>
          Status: <strong>{success.status}</strong>
        </p>

        <button
          type="button"
          onClick={() => setSuccess(null)}
        >
          Make another booking
        </button>
      </div>
    )
  }

  return (
    <div className="booking-form-container">
      <h3>Book this destination</h3>

      <p className="booking-form-description">
        Choose your preferred travel date and number of travelers.
      </p>

      {error && (
        <div className="auth-error">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="auth-form-group">
          <label htmlFor="travel-date">Travel date</label>

          <input
            id="travel-date"
            type="date"
            min={getTodayDate()}
            value={travelDate}
            onChange={(event) => setTravelDate(event.target.value)}
            required
          />
        </div>

        <div className="auth-form-group">
          <label htmlFor="travelers">Number of travelers</label>

          <input
            id="travelers"
            type="number"
            min="1"
            max="20"
            value={travelers}
            onChange={(event) => setTravelers(event.target.value)}
            required
          />
        </div>

        <div className="booking-total">
          <span>Estimated total</span>

          <strong>
            {totalPrice.toLocaleString()} ETB
          </strong>
        </div>

        <button
          type="submit"
          className="auth-submit-button"
          disabled={loading || Number(travelers) < 1 || Number(travelers) > 20}
        >
          {loading ? 'Submitting booking...' : 'Confirm booking'}
        </button>
      </form>
    </div>
  )
}

export default BookingForm
