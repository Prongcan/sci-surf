import { useQuery } from '@tanstack/react-query'
import { getFeaturedPapers, getRecommendations, type RecommendedPaper } from '../api/digests'
import { useAuthStore } from '../stores/auth'

export function useRecommendations() {
  const user = useAuthStore((s) => s.user)
  const isLoggedIn = useAuthStore((s) => s.isLoggedIn)
  const username = user?.username

  return useQuery<RecommendedPaper[]>({
    queryKey: ['recommendations', isLoggedIn ? username : 'featured'],
    queryFn: () => isLoggedIn && username ? getRecommendations(username) : getFeaturedPapers(),
    staleTime: 5 * 60 * 1000,
  })
}
