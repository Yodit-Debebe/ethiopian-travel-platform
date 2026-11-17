import DestinationCard from '../destinations/DestinationCard'

function HomePage({
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
  isInWishlist,
  wishlistActionId,
  formatCategory,
  handleWishlistToggle,
  openDestination,
}) {
  return (
    <>
      {/* Hero section */}
      <section className="hero" id="home">
        <div className="hero-overlay"></div>

        <div className="hero-content">
          <span className="eyebrow hero-eyebrow">
            <span className="eyebrow-dot"></span>
            DISCOVER THE LAND OF ORIGINS
          </span>

          <h1>
            Your next journey
            <br />
            begins in <span>Ethiopia.</span>
          </h1>

          <p className="hero-description">
            From ancient wonders to breathtaking landscapes, discover
            unforgettable places and experiences across Ethiopia.
          </p>

          <a href="#destinations" className="hero-button">
            Explore destinations <span>→</span>
          </a>

          <div className="hero-trust">
            <div className="avatar-stack">
              <span>Y</span>
              <span>A</span>
              <span>M</span>
            </div>

            <p>
              <strong>Discover more.</strong> Experience Ethiopia.
            </p>
          </div>
        </div>

        <div className="hero-location">
          <span className="location-pin">⌖</span>
          <span>Explore the beauty of Ethiopia</span>
        </div>
      </section>

      {/* Search section */}
      <section className="search-section">
        <div className="search-intro">
          <span className="section-kicker">PLAN YOUR JOURNEY</span>
          <h2>Where would you like to go?</h2>
        </div>

        <form
          className="search-box"
          onSubmit={(event) => {
            event.preventDefault()

            document
              .getElementById('destinations')
              ?.scrollIntoView({ behavior: 'smooth' })
          }}
        >
          <span className="search-icon">⌕</span>

          <input
            type="search"
            placeholder="Search destinations..."
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            aria-label="Search destinations"
          />

          <button type="submit">Search places</button>
        </form>
      </section>

      {/* Destinations section */}
      <section className="destinations-section" id="destinations">
        <div className="section-heading">
          <div>
            <span className="section-kicker">EXPLORE ETHIOPIA</span>
            <h2>Popular destinations</h2>
            <p>Find your next unforgettable experience.</p>
          </div>

          <a href="#destinations" className="view-all">
            Discover all places <span>→</span>
          </a>
        </div>

        <div className="category-list">
          {categories.map((category) => (
            <button
              key={category.value}
              className={
                activeCategory === category.value
                  ? 'category-button selected'
                  : 'category-button'
              }
              aria-pressed={activeCategory === category.value}
              onClick={() => setActiveCategory(category.value)}
              type="button"
            >
              {category.label}
            </button>
          ))}
        </div>

        {/* Destination sorting */}
        <div className="sorting-container">
          <label htmlFor="destination-sort">
            Sort destinations:
          </label>

          <select
            id="destination-sort"
            value={sortBy}
            onChange={(event) => setSortBy(event.target.value)}
          >
            <option value="default">Recommended</option>
            <option value="price-low">Price: Low to High</option>
            <option value="price-high">Price: High to Low</option>
            <option value="rating">Highest Rated</option>
            <option value="name">Name: A–Z</option>
          </select>
        </div>

        {wishlistError && (
          <div className="wishlist-error">
            <p>{wishlistError}</p>
            <button
              type="button"
              onClick={() => setWishlistError('')}
            >
              Dismiss
            </button>
          </div>
        )}

        <div className="destination-grid">
          {loading ? (
            <p>Loading destinations...</p>
          ) : error ? (
            <div className="empty-results">
              <h3>Something went wrong</h3>
              <p>{error}</p>

              <button
                type="button"
                onClick={() => window.location.reload()}
              >
                Try again
              </button>
            </div>
          ) : filteredDestinations.length > 0 ? (
            filteredDestinations.map((destination) => (
              <DestinationCard
                key={destination.id}
                destination={destination}
                saved={isInWishlist(destination.id)}
                isUpdating={wishlistActionId === destination.id}
                formatCategory={formatCategory}
                onWishlistToggle={handleWishlistToggle}
                onOpenDestination={openDestination}
              />
            ))
          ) : (
            <div className="empty-results">
              <h3>No destinations found</h3>
              <p>
                Try another search or choose a different category.
              </p>

              <button
                type="button"
                onClick={() => {
                  setSearch('')
                  setActiveCategory('All')
                }}
              >
                Clear filters
              </button>
            </div>
          )}
        </div>
      </section>

      {/* Recently viewed destinations */}
      {!loading && recentlyViewedDestinations.length > 0 && (
        <section className="destinations-section recently-viewed-section">
          <div className="section-heading">
            <div>
              <span className="section-kicker">
                YOUR EXPLORATION HISTORY
              </span>

              <h2>Recently viewed destinations</h2>

              <p>
                Pick up where you left off and continue exploring.
              </p>
            </div>

            <button
              type="button"
              className="clear-history-button"
              onClick={() => setRecentlyViewedIds([])}
            >
              Clear history
            </button>
          </div>

          <div className="destination-grid">
            {recentlyViewedDestinations.map((destination) => (
              <DestinationCard
                key={destination.id}
                destination={destination}
                saved={isInWishlist(destination.id)}
                isUpdating={wishlistActionId === destination.id}
                formatCategory={formatCategory}
                onWishlistToggle={handleWishlistToggle}
                onOpenDestination={openDestination}
              />
            ))}
          </div>
        </section>
      )}

      {/* About section */}
      <section className="experience-section" id="about">
        <div>
          <span className="section-kicker">
            MORE THAN A DESTINATION
          </span>

          <h2>Experience Ethiopia beyond the ordinary.</h2>

          <p>
            Explore remarkable heritage, welcoming communities, and
            landscapes that tell a thousand stories.
          </p>
        </div>

        <a href="#destinations" className="experience-button">
          Start exploring <span>→</span>
        </a>
      </section>
    </>
  )
}

export default HomePage
