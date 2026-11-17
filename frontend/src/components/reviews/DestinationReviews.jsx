
import { useEffect, useState } from 'react'
import { apiRequest } from '../../services/api'

function DestinationReviews({ destinationId }) {
  const [reviews, setReviews] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false

    async function loadReviews() {
      setLoading(true)
      setError('')

      try {
        let data = await apiRequest(
          `/api/reviews/?destination=${destinationId}`,
        )

        let allReviews = data.results ?? data

        // Load any additional pages if the API is paginated.
        let nextPage = data.next

        while (nextPage) {
          const nextUrl = new URL(
            nextPage,
            'http://127.0.0.1:8000'
          )

          if (nextUrl.origin !== 'http://127.0.0.1:8000') {
            throw new Error('Unexpected pagination URL.')
          }

          data = await apiRequest(
            `${nextUrl.pathname}${nextUrl.search}`
          )

          allReviews = [...allReviews, ...(data.results ?? data)]
          nextPage = data.next
        }

        if (!cancelled) {
          setReviews(allReviews)
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || 'Unable to load reviews.')
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadReviews()

    return () => {
      cancelled = true
    }
  }, [destinationId])

  return (
    <section className="destination-reviews">
      <div className="reviews-heading">
        <span className="section-kicker">TRAVELER FEEDBACK</span>
        <h2>Traveler Reviews</h2>
        <p>See what other travelers think about this destination.</p>
      </div>

      {loading ? (
        <p>Loading reviews...</p>
      ) : error ? (
        <p className="reviews-error">{error}</p>
      ) : reviews.length === 0 ? (
        <p className="no-reviews">
          No approved reviews yet. Be the first to share your experience!
        </p>
      ) : (
        <div className="reviews-list">
          {reviews.map((review) => (
            <article className="review-card" key={review.id}>
              <div className="review-card-header">
                <div>
                  <h3>{review.username}</h3>
                  <span>
                    {new Date(review.created_at).toLocaleDateString()}
                  </span>
                </div>

                <div
                  className="review-stars"
                  aria-label={`${review.rating} out of 5 stars`}
                >
                  {'★'.repeat(review.rating)}
                  <span>{'☆'.repeat(5 - review.rating)}</span>
                </div>
              </div>

              <p>{review.comment}</p>
            </article>
          ))}
        </div>
      )}
    </section>
  )
}

export default DestinationReviews
