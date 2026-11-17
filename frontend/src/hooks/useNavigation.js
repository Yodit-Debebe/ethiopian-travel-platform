
import { useState } from 'react'

function useNavigation(setSelectedDestination) {
  const [authPage, setAuthPage] = useState('home')
  const [accountMenuOpen, setAccountMenuOpen] = useState(false)

  const navigateTo = (page) => {
    setAuthPage(page)
    setSelectedDestination(null)
    setAccountMenuOpen(false)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const goHome = () => navigateTo('home')
  const openLogin = () => navigateTo('login')
  const openRegister = () => navigateTo('register')
  const openMyBookings = () => navigateTo('my-bookings')
  const openMyProfile = () => navigateTo('my-profile')
  const openMyPayments = () => navigateTo('my-payments')
  const openMyReviews = () => navigateTo('my-reviews')
  const openMyWishlist = () => navigateTo('my-wishlist')

  const closeAccountMenu = () => setAccountMenuOpen(false)

  const toggleAccountMenu = () => {
    setAccountMenuOpen((previous) => !previous)
  }

  return {
    authPage,
    setAuthPage,
    accountMenuOpen,
    setAccountMenuOpen,
    closeAccountMenu,
    toggleAccountMenu,
    goHome,
    openLogin,
    openRegister,
    openMyBookings,
    openMyProfile,
    openMyPayments,
    openMyReviews,
    openMyWishlist,
  }
}

export default useNavigation