import { useEffect, useState } from 'react'
import { getCurrentUser } from '../services/auth'
import { apiRequest } from '../services/api'

function useAuth() {
  const [currentUser, setCurrentUser] = useState(() => getCurrentUser())
  const currentUserId = currentUser?.id

  // Fetch the latest profile information
  useEffect(() => {
    const controller = new AbortController()

    async function fetchCurrentProfile() {
      if (!currentUserId) return

      try {
        const data = await apiRequest('/accounts/api/profile/', {
          signal: controller.signal,
        })

        setCurrentUser((previousUser) => {
          if (!previousUser) return previousUser

          return {
            ...previousUser,
            ...data,
          }
        })
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error('Failed to fetch profile information:', err)
        }
      }
    }

    fetchCurrentProfile()

    return () => controller.abort()
  }, [currentUserId])

  // Synchronize the current user with local storage
  useEffect(() => {
    if (currentUser) {
      localStorage.setItem(
        'currentUser',
        JSON.stringify(currentUser)
      )
    }
  }, [currentUser])

  // Update the current user's profile
  const handleProfileUpdated = (updatedUser) => {
    setCurrentUser((previousUser) => {
      if (!previousUser) return previousUser

      return {
        ...previousUser,
        ...updatedUser,
      }
    })
  }

  return {
    currentUser,
    setCurrentUser,
    handleProfileUpdated,
  }
}

export default useAuth