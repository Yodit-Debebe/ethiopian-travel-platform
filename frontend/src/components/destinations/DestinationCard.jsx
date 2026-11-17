function DestinationCard({
  destination,
  saved,
  isUpdating,
  formatCategory,
  onWishlistToggle,
  onOpenDestination,
}) {
  return (
    <article className="destination-card">
      <div className="destination-image">
        <img
          src={destination.img}
          alt={destination.name}
          loading="lazy"
        />

        <span className="image-category">
          {formatCategory(destination.category)}
        </span>

        <button
          className={
            saved
              ? 'favorite-button favorite-active'
              : 'favorite-button'
          }
          type="button"
          aria-label={
            saved
              ? `Remove ${destination.name} from wishlist`
              : `Save ${destination.name} to wishlist`
          }
          title={
            saved
              ? 'Remove from wishlist'
              : 'Add to wishlist'
          }
          aria-pressed={saved}
          disabled={isUpdating}
          onClick={() => onWishlistToggle(destination)}
        >
          {isUpdating ? '...' : saved ? '♥' : '♡'}
        </button>
      </div>

      <div className="destination-info">
        <div className="destination-title-row">
          <h3>{destination.name}</h3>

          <span
            className="rating"
            role="img"
            aria-label={
              destination.review_count > 0
                ? `Rated ${Number(destination.average_rating).toFixed(1)} out of 5`
                : 'No reviews yet'
            }
          >
            {destination.review_count > 0
              ? `★ ${Number(
                  destination.average_rating,
                ).toFixed(1)}`
              : 'New'}
          </span>
        </div>

        <p className="destination-region">
          {destination.desc}
        </p>

        <div className="destination-footer">
          <p>
            <strong>
              {Number(destination.price).toLocaleString()} ETB
            </strong>

            <span> / person</span>
          </p>

          <button
            type="button"
            className="details-link"
            onClick={() => onOpenDestination(destination)}
          >
            View details →
          </button>
        </div>
      </div>
    </article>
  )
}

export default DestinationCard