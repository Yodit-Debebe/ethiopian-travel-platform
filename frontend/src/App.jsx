import { useState } from 'react'
import './styles/index.css'

import Navbar from './components/layout/Navbar'
import PageContent from './components/layout/PageContent'
import useRecentlyViewed from './hooks/useRecentlyViewed'
import useWishlist from './hooks/useWishlist'
import useDestinations from './hooks/useDestinations'
import useDestinationView from './hooks/useDestinationView'
import useAuth from './hooks/useAuth'
import useNavigation from './hooks/useNavigation'
import useDestinationNavigation from './hooks/useDestinationNavigation'

import { logoutUser } from './services/auth'

const categories = [
  { label: 'All places', value: 'All' },
  { label: 'Historical', value: 'HISTORICAL' },
  { label: 'Nature', value: 'NATURAL' },
  { label: 'Lake', value: 'LAKE' },
  { label: 'Cultural', value: 'CULTURAL' },
  { label: 'Adventure', value: 'ADVENTURE' },
  { label: 'Other', value: 'OTHER' },
]

const formatCategory = (category) => {
  const categoryMap = {
    HISTORICAL: 'Historical',
    NATURAL: 'Nature',
    LAKE: 'Lake',
    CULTURAL: 'Cultural',
    ADVENTURE: 'Adventure',
    OTHER: 'Other',
  }

  return categoryMap[category] || category
}

function App() {
  
  const [currentYear] = useState(() => new Date().getFullYear())
  const [search, setSearch] = useState('')
  const [activeCategory, setActiveCategory] = useState('All')
  const [sortBy, setSortBy] = useState('default')
  const [selectedDestination, setSelectedDestination] = useState(null)

  const {
  destinations,
  loading,
  error,
  setError,
  } = useDestinations()

  // Recently viewed destinations
  const {
    recentlyViewedIds,
    setRecentlyViewedIds,
  } = useRecentlyViewed()

  const {
  filteredDestinations,
  recentlyViewedDestinations,
  relatedDestinations,
  } = useDestinationView({
    destinations,
    search,
    activeCategory,
    sortBy,
    recentlyViewedIds,
    selectedDestination,
  })

  // Authentication and page state
  const {
    currentUser,
    setCurrentUser,
    handleProfileUpdated,
  } = useAuth()

  const {
    authPage,
    setAuthPage,
    accountMenuOpen,
    goHome,
    closeAccountMenu,
    toggleAccountMenu,
    openLogin,
    openRegister,
    openMyBookings,
    openMyProfile,
    openMyPayments,
    openMyReviews,
    openMyWishlist,
  } = useNavigation(setSelectedDestination)

    const {
    wishlistItems,
    setWishlistItems,
    wishlistActionId,
    wishlistError,
    setWishlistError,
    isInWishlist,
    handleWishlistToggle,
  } = useWishlist(currentUser, openLogin)

  const {
    openDestination,
    openWishlistDestination,
    closeDestination,
  } = useDestinationNavigation({
    destinations,
    setAuthPage,
    setSelectedDestination,
    setRecentlyViewedIds,
    setError,
  })

  // Successful login
  const handleLogin = (user) => {
    closeAccountMenu()
    setCurrentUser(user)
    setAuthPage('home')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  // Logout
  const handleLogout = async () => {
    closeAccountMenu()
    try {
      await logoutUser()
    } catch (err) {
      console.error('Logout request failed:', err)
    } finally {
      setCurrentUser(null)
      setWishlistItems([])
      setSelectedDestination(null)
      setAuthPage('home')
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }
  return (
    <div className="app">
      <Navbar
        currentUser={currentUser}
        wishlistCount={wishlistItems.length}
        accountMenuOpen={accountMenuOpen}
        onToggleAccountMenu={toggleAccountMenu}
        onCloseAccountMenu={closeAccountMenu}
        onHome={goHome}
        onLogin={openLogin}
        onRegister={openRegister}
        onOpenProfile={openMyProfile}
        onOpenBookings={openMyBookings}
        onOpenPayments={openMyPayments}
        onOpenReviews={openMyReviews}
        onOpenWishlist={openMyWishlist}
        onLogout={handleLogout}
      />
      
      <main>
        <PageContent
          authPage={authPage}
          selectedDestination={selectedDestination}
          currentUser={currentUser}
          relatedDestinations={relatedDestinations}
          isInWishlist={isInWishlist}
          wishlistActionId={wishlistActionId}
          formatCategory={formatCategory}
          handleWishlistToggle={handleWishlistToggle}
          openDestination={openDestination}
          closeDestination={closeDestination}
          openLogin={openLogin}
          openRegister={openRegister}
          goHome={goHome}
          handleLogin={handleLogin}
          handleProfileUpdated={handleProfileUpdated}
          openWishlistDestination={openWishlistDestination}
          setWishlistItems={setWishlistItems}
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
        />
      </main>

      <footer className="footer">
        <a
          href="#home"
          className="brand footer-brand"
          onClick={goHome}
        >
          <span className="brand-mark">E</span>
          <span>
            Ethio<span className="brand-highlight">Explore</span>
          </span>
        </a>

        <p>Discover Ethiopia. Create unforgettable memories.</p>

        <span>© {currentYear} EthioExplore</span>
      </footer>
    </div>
  )
}

export default App
