import { useEffect, useState } from 'react'
import { apiRequest } from '../services/api'

function useWishlist(currentUser, onUnauthenticated) {
  const [wishlistItems, setWishlistItems] = useState([])
  const [wishlistLoading, setWishlistLoading] = useState(false)
  const [wishlistActionId, setWishlistActionId] = useState(null)
  const [wishlistError, setWishlistError] = useState('')
  const currentUserId = currentUser?.id

  // Fetch the logged-in user's wishlist
  useEffect(() => {
    const controller = new AbortController()

    async function fetchWishlist() {
        if (!currentUserId) {
        setWishlistItems([])
        setWishlistLoading(false)
        return
      }

      try {
        setWishlistLoading(true)
        setWishlistError('')

        const data = await apiRequest('/api/wishlist/', {
          signal: controller.signal,
        })

        setWishlistItems(data.results ?? data)
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error('Failed to load wishlist:', err)
          setWishlistError(err.message || 'Unable to load wishlist.')
        }
      } finally {
        if (!controller.signal.aborted) {
          setWishlistLoading(false)
        }
      }
    }

    fetchWishlist()

    return () => controller.abort()
    }, [currentUserId])

  // Check whether a destination is already in the wishlist
  const isInWishlist = (destinationId) => {
    return wishlistItems.some(
      (item) => Number(item.destination) === Number(destinationId)
    )
  }

  // Add or remove a destination from the wishlist
  const handleWishlistToggle = async (destination) => {
    if (!currentUser) {
      onUnauthenticated()
      return
    }

    const existingItem = wishlistItems.find(
      (item) => Number(item.destination) === Number(destination.id)
    )

    try {
      setWishlistActionId(destination.id)
      setWishlistError('')

      if (existingItem) {
        await apiRequest(`/api/wishlist/${existingItem.id}/`, {
          method: 'DELETE',
        })

        setWishlistItems((previousItems) =>
          previousItems.filter(
            (item) => Number(item.id) !== Number(existingItem.id)
          )
        )
      } else {
        const newItem = await apiRequest('/api/wishlist/', {
          method: 'POST',
          body: JSON.stringify({
            destination: destination.id,
          }),
        })

        setWishlistItems((previousItems) => [
          newItem,
          ...previousItems,
        ])
      }
    } catch (err) {
      console.error('Wishlist action failed:', err)

      setWishlistError(
        err.message || 'Unable to update your wishlist.'
      )
    } finally {
      setWishlistActionId(null)
    }
  }

  return {
    wishlistItems,
    setWishlistItems,
    wishlistLoading,
    wishlistActionId,
    wishlistError,
    setWishlistError,
    isInWishlist,
    handleWishlistToggle,
  }
}

export default useWishlist