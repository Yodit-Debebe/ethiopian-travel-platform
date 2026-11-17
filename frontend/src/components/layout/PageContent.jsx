import Login from '../auth/Login'
import Register from '../auth/Register'
import MyBookings from '../bookings/MyBookings'
import PaymentManagement from '../payments/PaymentManagement'
import ReviewManagement from '../reviews/ReviewManagement'
import Wishlist from '../wishlist/Wishlist'
import Profile from '../profile/Profile'
import DestinationDetails from '../destinations/DestinationDetails'
import HomePage from '../home/HomePage'

function PageContent({
  authPage,
  selectedDestination,
  currentUser,
  relatedDestinations,
  isInWishlist,
  wishlistActionId,
  formatCategory,
  handleWishlistToggle,
  openDestination,
  closeDestination,
  openLogin,
  openRegister,
  goHome,
  handleLogin,
  handleProfileUpdated,
  openWishlistDestination,
  setWishlistItems,
  categories,
  search,
  setSearch,
  activeCategory,
  setActiveCategory,
  sortBy,
  setSortBy,
  wishlistError,
  setWishlistError,
  loading,
  error,
  filteredDestinations,
  recentlyViewedDestinations,
  setRecentlyViewedIds,
}) {
  if (authPage === 'login') {
    return (
      <Login
        onLogin={handleLogin}
        onSwitchToRegister={openRegister}
        onBack={goHome}
      />
    )
  }

  if (authPage === 'register') {
    return (
      <Register
        onSwitchToLogin={openLogin}
        onBack={goHome}
      />
    )
  }

  if (authPage === 'my-profile') {
    return (
      <Profile
        onBack={goHome}
        onProfileUpdated={handleProfileUpdated}
      />
    )
  }

  if (authPage === 'my-reviews') {
    return (
      <ReviewManagement
        currentUser={currentUser}
        onBack={goHome}
      />
    )
  }

  if (authPage === 'my-payments') {
    return <PaymentManagement onBack={goHome} />
  }

  if (authPage === 'my-bookings') {
    return <MyBookings onBack={goHome} />
  }

  if (authPage === 'my-wishlist') {
    return (
      <Wishlist
        onBack={goHome}
        onOpenDestination={openWishlistDestination}
        onWishlistChange={setWishlistItems}
      />
    )
  }

  if (selectedDestination) {
    return (
      <DestinationDetails
        destination={selectedDestination}
        currentUser={currentUser}
        relatedDestinations={relatedDestinations}
        isInWishlist={isInWishlist}
        wishlistActionId={wishlistActionId}
        formatCategory={formatCategory}
        handleWishlistToggle={handleWishlistToggle}
        openDestination={openDestination}
        closeDestination={closeDestination}
        openLogin={openLogin}
      />
    )
  }

  return (
    <HomePage
      categories={categories}
      search={search}
      setSearch={setSearch}
      activeCategory={activeCategory}
      setActiveCategory={setActiveCategory}
      sortBy={sortBy}
      setSortBy={setSortBy}
      wishlistError={wishlistError}
      setWishlistError={setWishlistError}
      loading={loading}
      error={error}
      filteredDestinations={filteredDestinations}
      recentlyViewedDestinations={recentlyViewedDestinations}
      setRecentlyViewedIds={setRecentlyViewedIds}
      isInWishlist={isInWishlist}
      wishlistActionId={wishlistActionId}
      formatCategory={formatCategory}
      handleWishlistToggle={handleWishlistToggle}
      openDestination={openDestination}
    />
  )
}

export default PageContent
