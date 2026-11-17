import { useMemo } from 'react'

function useDestinationView({
  destinations,
  search,
  activeCategory,
  sortBy,
  recentlyViewedIds,
  selectedDestination,
}) {
  const filteredDestinations = useMemo(() => {
    const searchTerm = search.toLowerCase()

    return destinations
      .filter((destination) => {
        const matchesSearch =
          destination.name.toLowerCase().includes(searchTerm) ||
          destination.desc.toLowerCase().includes(searchTerm)

        const matchesCategory =
          activeCategory === 'All' ||
          destination.category === activeCategory

        return matchesSearch && matchesCategory
      })
      .sort((a, b) => {
        switch (sortBy) {
          case 'price-low':
            return Number(a.price) - Number(b.price)

          case 'price-high':
            return Number(b.price) - Number(a.price)

          case 'rating':
            return (
              Number(b.average_rating || 0) -
              Number(a.average_rating || 0)
            )

          case 'name':
            return a.name.localeCompare(b.name)

          default:
            return 0
        }
      })
  }, [destinations, search, activeCategory, sortBy])

  const recentlyViewedDestinations = useMemo(() => {
    const destinationsById = new Map(
      destinations.map((destination) => [
        Number(destination.id),
        destination,
      ])
    )

    return recentlyViewedIds
      .map((id) => destinationsById.get(Number(id)))
      .filter(Boolean)
  }, [destinations, recentlyViewedIds])

  const relatedDestinations = useMemo(() => {
    if (!selectedDestination) return []

    return destinations
      .filter(
        (destination) =>
          destination.category === selectedDestination.category &&
          Number(destination.id) !== Number(selectedDestination.id)
      )
      .slice(0, 3)
  }, [destinations, selectedDestination])

  return {
    filteredDestinations,
    recentlyViewedDestinations,
    relatedDestinations,
  }
}

export default useDestinationView