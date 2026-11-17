
import { useCallback, useEffect, useState } from 'react'
import { apiRequest } from '../../services/api'

const API_BASE_URL = 'http://127.0.0.1:8000'

async function fetchAllPages(endpoint) {
  let nextUrl = endpoint
  const allItems = []

  while (nextUrl) {
    const url = new URL(nextUrl, API_BASE_URL)

if (url.origin !== API_BASE_URL) {
  throw new Error('Unexpected pagination URL.')
}

const path = `${url.pathname}${url.search}`

    const data = await apiRequest(path)

    if (Array.isArray(data)) {
      allItems.push(...data)
      break
    }

    allItems.push(...(data.results || []))
    nextUrl = data.next
  }

  return allItems
}

function ReviewManagement({ currentUser, onBack }) {
  const [bookings, setBookings] = useState([])
  const [payments, setPayments] = useState([])
  const [destinations, setDestinations] = useState([])
  const [myReviews, setMyReviews] = useState([])
  const [adminReviews, setAdminReviews] = useState([])

  const [selectedBooking, setSelectedBooking] = useState('')
  const [rating, setRating] = useState('5')
  const [comment, setComment] = useState('')

  const [editingReview, setEditingReview] = useState(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  const isAdmin = Boolean(
    currentUser?.is_staff || currentUser?.is_superuser
  )

  const loadData = useCallback(async () => {
    try {
      setLoading(true)
      setError('')

      const [
        bookingData,
        paymentData,
        destinationData,
        reviewData,
      ] = await Promise.all([
        fetchAllPages('/api/bookings/'),
        fetchAllPages('/api/payments/'),
        fetchAllPages('/api/destinations/'),
        fetchAllPages('/api/reviews/my/'),
      ])

      setBookings(bookingData)
      setPayments(paymentData)
      setDestinations(destinationData)
      setMyReviews(reviewData)

      if (isAdmin) {
        const adminData = await fetchAllPages('/api/reviews/admin/')
        setAdminReviews(adminData)
      }
    } catch (err) {
      console.error('Failed to load reviews:', err)
      setError(err.message || 'Unable to load review information.')
    } finally {
      setLoading(false)
    }
  }, [isAdmin])

  useEffect(() => {
    let isActive = true

    const loadInitialData = async () => {
      try {
        const [
          bookingData,
          paymentData,
          destinationData,
          reviewData,
        ] = await Promise.all([
          fetchAllPages('/api/bookings/'),
          fetchAllPages('/api/payments/'),
          fetchAllPages('/api/destinations/'),
          fetchAllPages('/api/reviews/my/'),
        ])

        if (!isActive) return

        setBookings(bookingData)
        setPayments(paymentData)
        setDestinations(destinationData)
        setMyReviews(reviewData)

        if (isAdmin) {
          const adminData = await fetchAllPages('/api/reviews/admin/')

          if (!isActive) return

          setAdminReviews(adminData)
        }
      } catch (err) {
        if (isActive) {
          console.error('Failed to load reviews:', err)
          setError(err.message || 'Unable to load review information.')
        }
      } finally {
        if (isActive) {
          setLoading(false)
        }
      }
    }

    loadInitialData()

    return () => {
      isActive = false
    }
  }, [isAdmin])

  const getDestinationName = (destinationId) => {
    const destination = destinations.find(
      (item) => item.id === Number(destinationId)
    )

    return destination?.name || `Destination #${destinationId}`
  }

    const [todayString] = useState(() => {
    const today = new Date()

    return [
      today.getFullYear(),
      String(today.getMonth() + 1).padStart(2, '0'),
      String(today.getDate()).padStart(2, '0'),
    ].join('-')
  })

  const eligibleBookings = bookings.filter((booking) => {
    const hasSuccessfulPayment = payments.some(
      (payment) =>
        payment.booking === booking.id &&
        payment.status === 'SUCCESSFUL'
    )

    const alreadyReviewed = myReviews.some(
      (review) => review.booking === booking.id
    )

    return (
      booking.status === 'CONFIRMED' &&
      booking.travel_date < todayString &&
      hasSuccessfulPayment &&
      !alreadyReviewed
    )
  })

  const handleSubmitReview = async (event) => {
    event.preventDefault()

    if (!selectedBooking || !comment.trim()) {
      setError('Please select a booking and enter a review.')
      return
    }

    try {
      setSubmitting(true)
      setError('')
      setMessage('')

      await apiRequest('/api/reviews/my/', {
        method: 'POST',
        body: JSON.stringify({
          booking: Number(selectedBooking),
          rating: Number(rating),
          comment: comment.trim(),
        }),
      })

      setMessage('Your review was submitted and is awaiting approval.')
      setSelectedBooking('')
      setRating('5')
      setComment('')

      await loadData()
    } catch (err) {
      setError(err.message || 'Failed to submit your review.')
    } finally {
      setSubmitting(false)
    }
  }

  const handleEditReview = async (event) => {
    event.preventDefault()

    if (!editingReview || !editingReview.comment.trim()) {
      setError('Please enter a review comment.')
      return
    }

    try {
      setSubmitting(true)
      setError('')
      setMessage('')

      await apiRequest(`/api/reviews/my/${editingReview.id}/`, {
        method: 'PATCH',
        body: JSON.stringify({
          rating: Number(editingReview.rating),
          comment: editingReview.comment.trim(),
        }),
      })

      setMessage('Your review was updated successfully.')
      setEditingReview(null)

      await loadData()
    } catch (err) {
      setError(err.message || 'Failed to update your review.')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDeleteReview = async (reviewId) => {
    const confirmed = window.confirm(
      'Are you sure you want to delete this review?'
    )

    if (!confirmed) return

    try {
      setError('')
      setMessage('')

      await apiRequest(`/api/reviews/my/${reviewId}/`, {
        method: 'DELETE',
      })

      setMessage('Your review was deleted successfully.')
      await loadData()
    } catch (err) {
      setError(err.message || 'Failed to delete your review.')
    }
  }

  const handleModeration = async (reviewId, newStatus) => {
    try {
      setError('')
      setMessage('')

      const response = await apiRequest(
        `/api/reviews/admin/${reviewId}/moderate/`,
        {
          method: 'PATCH',
          body: JSON.stringify({ status: newStatus }),
        }
      )

      setMessage(response.message || 'Review moderation completed.')
      await loadData()
    } catch (err) {
      setError(err.message || 'Failed to moderate this review.')
    }
  }

  const formatStatus = (status) => {
    return status.charAt(0) + status.slice(1).toLowerCase()
  }

  if (loading) {
    return (
      <section className="reviews-page">
        <p>Loading reviews...</p>
      </section>
    )
  }

  return (
    <section className="reviews-page">
      <button
        type="button"
        className="back-button"
        onClick={onBack}
      >
        ← Back
      </button>

      <div className="reviews-heading">
        <span className="section-kicker">CUSTOMER FEEDBACK</span>
        <h1>Reviews Management</h1>
        <p>Share your travel experiences and explore customer feedback.</p>
      </div>

      {error && <div className="reviews-error">{error}</div>}
      {message && <div className="reviews-message">{message}</div>}

      {!isAdmin && (
        <>
          <div className="review-section">
            <h2>Write a review</h2>
            <p>
              You can review a completed trip after successful payment.
            </p>

            {eligibleBookings.length === 0 ? (
              <div className="reviews-empty">
                You currently have no eligible bookings to review.
                Completed, confirmed, successfully paid trips will appear
                here.
              </div>
            ) : (
              <form
                className="review-form"
                onSubmit={handleSubmitReview}
              >
                <label htmlFor="review-booking">
                  Select a completed trip
                </label>

                <select
                  id="review-booking"
                  value={selectedBooking}
                  onChange={(event) =>
                    setSelectedBooking(event.target.value)
                  }
                  required
                >
                  <option value="">Choose a booking</option>

                  {eligibleBookings.map((booking) => (
                    <option key={booking.id} value={booking.id}>
                      {getDestinationName(booking.destination)}
                      {' - Booking #'}
                      {booking.id}
                    </option>
                  ))}
                </select>

                <label htmlFor="review-rating">Your rating</label>

                <select
                  id="review-rating"
                  value={rating}
                  onChange={(event) => setRating(event.target.value)}
                >
                  <option value="5">★★★★★ - Excellent</option>
                  <option value="4">★★★★☆ - Very good</option>
                  <option value="3">★★★☆☆ - Good</option>
                  <option value="2">★★☆☆☆ - Fair</option>
                  <option value="1">★☆☆☆☆ - Poor</option>
                </select>

                <label htmlFor="review-comment">
                  Your experience
                </label>

                <textarea
                  id="review-comment"
                  value={comment}
                  onChange={(event) => setComment(event.target.value)}
                  placeholder="Tell us about your trip..."
                  maxLength={1000}
                  rows={5}
                  required
                />

                <button
                  type="submit"
                  className="review-submit-button"
                  disabled={submitting}
                >
                  {submitting ? 'Submitting...' : 'Submit review'}
                </button>
              </form>
            )}
          </div>

          <div className="review-section">
            <h2>My reviews</h2>

            {myReviews.length === 0 ? (
              <div className="reviews-empty">
                You haven't submitted any reviews yet.
              </div>
            ) : (
              <div className="review-list">
                {myReviews.map((review) => (
                  <article className="review-card" key={review.id}>
                    {editingReview?.id === review.id ? (
                      <form onSubmit={handleEditReview}>
                        <label>Rating</label>

                        <select
                          value={editingReview.rating}
                          onChange={(event) =>
                            setEditingReview({
                              ...editingReview,
                              rating: event.target.value,
                            })
                          }
                        >
                          {[5, 4, 3, 2, 1].map((value) => (
                            <option key={value} value={value}>
                              {value} / 5
                            </option>
                          ))}
                        </select>

                        <label>Comment</label>

                        <textarea
                          value={editingReview.comment}
                          onChange={(event) =>
                            setEditingReview({
                              ...editingReview,
                              comment: event.target.value,
                            })
                          }
                          maxLength={1000}
                          required
                        />

                        <button
                          type="submit"
                          disabled={submitting}
                        >
                          Save changes
                        </button>

                        <button
                          type="button"
                          onClick={() => setEditingReview(null)}
                        >
                          Cancel
                        </button>
                      </form>
                    ) : (
                      <>
                        <div className="review-card-header">
                          <h3>
                            {review.destination_name ||
                              getDestinationName(review.destination)}
                          </h3>

                          <span className={`review-status ${review.status.toLowerCase()}`}>
                            {formatStatus(review.status)}
                          </span>
                        </div>

                        <div className="review-stars">
                          {'★'.repeat(review.rating)}
                          {'☆'.repeat(5 - review.rating)}
                        </div>

                        <p>{review.comment}</p>

                        <small>
                          Submitted:{' '}
                          {new Date(review.created_at).toLocaleDateString()}
                        </small>

                        {review.status !== 'APPROVED' && (
                          <div className="review-actions">
                            <button
                              type="button"
                              onClick={() =>
                                setEditingReview({
                                  id: review.id,
                                  rating: String(review.rating),
                                  comment: review.comment,
                                })
                              }
                            >
                              Edit
                            </button>

                            <button
                              type="button"
                              onClick={() =>
                                handleDeleteReview(review.id)
                              }
                            >
                              Delete
                            </button>
                          </div>
                        )}
                      </>
                    )}
                  </article>
                ))}
              </div>
            )}
          </div>
        </>
      )}

      {isAdmin && (
        <div className="review-section">
          <h2>Review moderation</h2>
          <p>Review customer submissions and manage their approval.</p>

          {adminReviews.filter(
            (review) => review.status === 'PENDING'
          ).length === 0 ? (
            <div className="reviews-empty">
              There are no pending reviews to moderate.
            </div>
          ) : (
            <div className="review-list">
              {adminReviews
                .filter((review) => review.status === 'PENDING')
                .map((review) => (
                  <article className="review-card" key={review.id}>
                    <div className="review-card-header">
                      <h3>
                        {review.destination_name ||
                          getDestinationName(review.destination)}
                      </h3>

                      <span className="review-status pending">
                        Pending
                      </span>
                    </div>

                    <p>
                      <strong>Customer:</strong> {review.username}
                    </p>

                    <div className="review-stars">
                      {'★'.repeat(review.rating)}
                      {'☆'.repeat(5 - review.rating)}
                    </div>

                    <p>{review.comment}</p>

                    <small>
                      Submitted:{' '}
                      {new Date(review.created_at).toLocaleDateString()}
                    </small>

                    <div className="review-actions">
                      <button
                        type="button"
                        className="approve-review-button"
                        onClick={() =>
                          handleModeration(review.id, 'APPROVED')
                        }
                      >
                        Approve
                      </button>

                      <button
                        type="button"
                        className="reject-review-button"
                        onClick={() =>
                          handleModeration(review.id, 'REJECTED')
                        }
                      >
                        Reject
                      </button>
                    </div>
                  </article>
                ))}
            </div>
          )}
        </div>
      )}
    </section>
  )
}

export default ReviewManagement
