import type { AppRouteMatch } from '@/types'
import { useMatches } from 'react-router-dom'

export const useAppMatches = () => useMatches() as AppRouteMatch[]
