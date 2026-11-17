import { useEffect, useState } from 'react'

function useRecentlyViewed() {
  const [recentlyViewedIds, setRecentlyViewedIds] = useState(() => {
    try {
      const storedIds = JSON.parse(
        localStorage.getItem('recentlyViewedIds')
      )

      return Array.isArray(storedIds) ? storedIds : []
    } catch {
      return []
    }
  })

  useEffect(() => {
    localStorage.setItem(
      'recentlyViewedIds',
      JSON.stringify(recentlyViewedIds)
    )
  }, [recentlyViewedIds])

  return {
    recentlyViewedIds,
    setRecentlyViewedIds,
  }
}

export default useRecentlyViewed