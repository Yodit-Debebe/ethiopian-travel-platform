import BookingForm from '../bookings/BookingForm'
import DestinationReviews from '../reviews/DestinationReviews'
import DestinationCard from './DestinationCard'

function DestinationDetails({
  destination,
  currentUser,
  relatedDestinations,
  isInWishlist,
  wishlistActionId,
  formatCategory,
  handleWishlistToggle,
  openDestination,
  closeDestination,
  openLogin,
}) {
  return (
    <section className="destination-details">
      <button
        className="back-button"
        type="button"
        onClick={closeDestination}
      >
        ← Back to destinations
      </button>

      <div className="details-layout">
        <div className="details-image">
          <img
            src={destination.img}
            alt={destination.name}
          />
        </div>

        <div className="details-content">
          <span className="section-kicker">
            EXPLORE ETHIOPIA
          </span>

          <span className="image-category">
            {formatCategory(destination.category)}
          </span>

          <h1>{destination.name}</h1>

          <div
            className="details-rating"
            role="img"
            aria-label={
                destination.review_count > 0
                ? `Rated ${Number(destination.average_rating).toFixed(1)} out of 5 based on ${destination.review_count} reviews`
                : 'No reviews yet'
            }
          >
            {destination.review_count > 0
              ? `★ ${Number(
                  destination.average_rating,
                ).toFixed(1)} (${destination.review_count} reviews)`
              : 'New destination'}
          </div>

          <p className="details-description">
            {destination.desc}
          </p>

          <div className="details-price">
            <span>Starting from</span>

            <h2>
              {Number(destination.price).toLocaleString()} ETB
            </h2>

            <p>per person</p>
          </div>

          {currentUser ? (
            <BookingForm destination={destination} />
          ) : (
            <button
              type="button"
              className="details-book-button"
              onClick={openLogin}
            >
              Log in to book this destination →
            </button>
          )}
        </div>
      </div>

      <DestinationReviews destinationId={destination.id} />

      <section className="related-destinations">
        <div className="section-heading">
          <div>
            <span className="section-kicker">
              KEEP EXPLORING
            </span>

            <h2>Related destinations</h2>

            <p>
              Discover more places in the same category.
            </p>
          </div>
        </div>

        {relatedDestinations.length > 0 ? (
          <div className="destination-grid">
            {relatedDestinations.map((relatedDestination) => (
              <DestinationCard
                key={relatedDestination.id}
                destination={relatedDestination}
                saved={isInWishlist(relatedDestination.id)}
                isUpdating={
                  wishlistActionId != null &&
                  Number(wishlistActionId) === Number(relatedDestination.id)
                }
                formatCategory={formatCategory}
                onWishlistToggle={handleWishlistToggle}
                onOpenDestination={openDestination}
              />
            ))}
          </div>
        ) : (
          <div className="empty-results">
            <h3>No related destinations yet</h3>
            <p>
              We don't have other destinations in this category
              right now. Check back later for more places to explore.
            </p>
          </div>
        )}
      </section>
    </section>
  )
}

export default DestinationDetails