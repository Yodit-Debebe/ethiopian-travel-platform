import { useCallback, useEffect, useState } from 'react'
import { apiRequest } from '../../services/api'

function Wishlist({ onBack, onOpenDestination, onWishlistChange }) {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [removingId, setRemovingId] = useState(null)

  const fetchWishlist = useCallback(async () => {
    try {
      setLoading(true)
      setError('')

      const data = await apiRequest('/api/wishlist/')
      const wishlistItems = data.results ?? data

      setItems(wishlistItems)
      onWishlistChange?.(wishlistItems)
    } catch (err) {
      setError(err.message || 'Unable to load your wishlist.')
    } finally {
      setLoading(false)
    }
  }, [onWishlistChange])

  useEffect(() => {
    let isActive = true

    const loadInitialWishlist = async () => {
      try {
        const data = await apiRequest('/api/wishlist/')
        const wishlistItems = data.results ?? data

        if (!isActive) return

        setItems(wishlistItems)
        onWishlistChange?.(wishlistItems)
      } catch (err) {
        if (!isActive) return

        setError(err.message || 'Unable to load your wishlist.')
      } finally {
        if (isActive) {
          setLoading(false)
        }
      }
    }

    loadInitialWishlist()

    return () => {
      isActive = false
    }
  }, [onWishlistChange])

  const handleRemove = async (itemId) => {
    try {
      setRemovingId(itemId)
      setError('')

      await apiRequest(`/api/wishlist/${itemId}/`, {
        method: 'DELETE',
      })

      const updatedItems = items.filter(
        (item) => item.id !== itemId
      )

      setItems(updatedItems)
      onWishlistChange?.(updatedItems)
    } catch (err) {
      setError(err.message || 'Unable to remove this destination.')
    } finally {
      setRemovingId(null)
    }
  }

  return (
    <section className="wishlist-page">
      <button
        type="button"
        className="back-button"
        onClick={onBack}
      >
        ← Back to destinations
      </button>

      <div className="wishlist-heading">
        <span className="section-kicker">YOUR SAVED PLACES</span>
        <h1>My Wishlist</h1>
        <p>
          Keep track of the Ethiopian destinations you would love to visit.
        </p>
      </div>

      {loading ? (
        <p className="wishlist-message">Loading your wishlist...</p>
      ) : error ? (
        <div className="wishlist-error">
          <p>{error}</p>
          <button type="button" onClick={fetchWishlist}>
            Try again
          </button>
        </div>
      ) : items.length === 0 ? (
        <div className="wishlist-empty">
          <span>♡</span>
          <h2>Your wishlist is empty</h2>
          <p>
            Explore destinations and save the places you would like to visit.
          </p>
          <button type="button" onClick={onBack}>
            Explore destinations
          </button>
        </div>
      ) : (
        <>
          <p className="wishlist-count">
            {items.length} saved{' '}
            {items.length === 1 ? 'destination' : 'destinations'}
          </p>

          <div className="wishlist-grid">
            {items.map((item) => (
              <article className="wishlist-card" key={item.id}>
                <div className="wishlist-card-image">
                  <img
                    src={item.destination_image}
                    alt={item.destination_name}
                    loading="lazy"
                  />
                </div>

                <div className="wishlist-card-info">
                  <h3>{item.destination_name}</h3>

                  <p>
                    {Number(item.destination_price).toLocaleString()} ETB
                    <span> / person</span>
                  </p>

                  <div className="wishlist-card-actions">
                    <button
                      type="button"
                      onClick={() =>
                        onOpenDestination(item.destination)
                      }
                    >
                      View details
                    </button>

                    <button
                      type="button"
                      className="wishlist-remove"
                      disabled={removingId === item.id}
                      onClick={() => handleRemove(item.id)}
                    >
                      {removingId === item.id
                        ? 'Removing...'
                        : 'Remove ♡'}
                    </button>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </>
      )}
    </section>
  )
}

export default Wishlist
