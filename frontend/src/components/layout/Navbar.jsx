import { useState } from 'react'

function Navbar({
  currentUser,
  wishlistCount,
  accountMenuOpen,
  onToggleAccountMenu,
  onCloseAccountMenu,
  onHome,
  onLogin,
  onRegister,
  onOpenProfile,
  onOpenBookings,
  onOpenPayments,
  onOpenReviews,
  onOpenWishlist,
  onLogout,
}) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleNavigation = () => {
    setMobileMenuOpen(false)
    onHome()
  }

  return (
    <header className="navbar">
      <a
        href="#home"
        className="brand"
        onClick={handleNavigation}
      >
        <span className="brand-mark">E</span>
        <span>
          Ethio<span className="brand-highlight">Explore</span>
        </span>
      </a>

      <nav
        className={`nav-links ${mobileMenuOpen ? 'mobile-open' : ''}`}
        id="primary-navigation"
        aria-label="Main navigation"
      >
        <a
          className="active-link"
          href="#home"
          onClick={handleNavigation}
        >
          Home
        </a>

        <a
          href="#destinations"
          onClick={handleNavigation}
        >
          Destinations
        </a>

        <a
          href="#about"
          onClick={handleNavigation}
        >
          About us
        </a>
      </nav>

      <button
        type="button"
        className="mobile-menu-toggle"
        onClick={() => setMobileMenuOpen((open) => !open)}
        aria-label={mobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
        aria-expanded={mobileMenuOpen}
        aria-controls="primary-navigation"
      >
        <span />
        <span />
        <span />
      </button>

      <div className="nav-actions">
        {currentUser ? (
          <div className="account-menu">
            <button
              type="button"
              className="account-menu-trigger"
              onClick={() => {
                setMobileMenuOpen(false)
                onToggleAccountMenu()
              }}
              aria-expanded={accountMenuOpen}
              aria-haspopup="true"
              aria-controls="account-dropdown"
              aria-label="Open account menu"
            >
              <span className="account-avatar">
                {currentUser.profile_picture_url ? (
                  <img
                    src={currentUser.profile_picture_url}
                    alt=""
                  />
                ) : (
                  currentUser.username?.charAt(0).toUpperCase() || '?'
                )}
              </span>

              <span className="account-username">
                {currentUser.username}
              </span>

              <span className={`account-chevron ${accountMenuOpen ? 'open' : ''}`}>
                ▾
              </span>
            </button>

            {accountMenuOpen && (
              <div
                className="account-dropdown"
                id="account-dropdown"
              >
                <div className="account-dropdown-header">
                  <strong>{currentUser.username}</strong>
                  <span>Manage your account</span>
                </div>

                <button
                  type="button"
                  onClick={() => {
                    onCloseAccountMenu()
                    onOpenProfile()
                  }}
                >
                  <span>👤</span> My Profile
                </button>

                <button
                  type="button"
                  onClick={() => {
                    onCloseAccountMenu()
                    onOpenBookings()
                  }}
                >
                  <span>📅</span> My Bookings
                </button>

                <button
                  type="button"
                  onClick={() => {
                    onCloseAccountMenu()
                    onOpenPayments()
                  }}
                >
                  <span>💳</span> My Payments
                </button>

                <button
                  type="button"
                  onClick={() => {
                    onCloseAccountMenu()
                    onOpenReviews()
                  }}
                >
                  <span>⭐</span>
                  {currentUser.is_staff || currentUser.is_superuser
                    ? 'Review Moderation'
                    : 'My Reviews'}
                </button>

                <button
                  type="button"
                  onClick={() => {
                    onCloseAccountMenu()
                    onOpenWishlist()
                  }}
                >
                  <span>♥</span>
                  My Wishlist
                  {wishlistCount > 0 ? ` (${wishlistCount})` : ''}
                </button>

                <div className="account-dropdown-divider" />

                <button
                  type="button"
                  className="account-logout"
                  onClick={() => {
                    onCloseAccountMenu()
                    onLogout()
                  }}
                >
                  <span>↪</span> Log out
                </button>
              </div>
            )}
          </div>
        ) : (
          <>
            <button
              type="button"
              className="login-link"
              onClick={() => {
                setMobileMenuOpen(false)
                onLogin()
              }}
            >
              Log in
            </button>

            <button
              type="button"
              className="nav-button"
              onClick={() => {
                setMobileMenuOpen(false)
                onRegister()
              }}
            >
              Sign up
            </button>
          </>
        )}
      </div>
    </header>
  )
}

export default Navbar
