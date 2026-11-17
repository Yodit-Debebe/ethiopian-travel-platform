
function useDestinationNavigation({
  destinations,
  setSelectedDestination,
  setAuthPage,
  setRecentlyViewedIds,
  setError,
}) {
  const openDestination = (destination) => {
    setAuthPage('home')
    setSelectedDestination(destination)

    setRecentlyViewedIds((previousIds) => [
      destination.id,
      ...previousIds.filter(
  (id) => Number(id) !== Number(destination.id)
),
    ].slice(0, 5))

    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const openWishlistDestination = (destinationId) => {
    const destination = destinations.find(
      (item) => Number(item.id) === Number(destinationId)
    )

    if (destination) {
      openDestination(destination)
    } else {
      setAuthPage('home')
      setSelectedDestination(null)
      setError('This destination could not be found.')
    }
  }

  const closeDestination = () => {
    setSelectedDestination(null)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return {
    openDestination,
    openWishlistDestination,
    closeDestination,
  }
}

export default useDestinationNavigation
