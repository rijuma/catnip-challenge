import type { IndexRouteObject, NonIndexRouteObject, UIMatch } from 'react-router'

// My custom type for route handles
export type AppRouteHandle = {
  crumb?: string | Function
  sidebarPath?: string
}

export type AppRouteMatch = UIMatch<unknown, AppRouteHandle>

export type AppIndexRouteObject = Omit<IndexRouteObject, 'handle'> & {
  handle?: AppRouteHandle
}

export type AppNonIndexRouteObject = Omit<NonIndexRouteObject, 'handle' | 'children'> & {
  handle?: AppRouteHandle
  children?: AppRouteObject[]
}

export type AppRouteObject = AppIndexRouteObject | AppNonIndexRouteObject
