// src/App.jsx
import SidebarLayout from '@/layouts/sidebar-layout'
import HomePage from '@/pages/home-page'
import UsersPage from '@/pages/users-page'
import UserDetailsPage from '@/pages/user-details-page'
import UsersNewPage from '@/pages/users-new-page'
import type { AppRouteObject } from '@/types'

export const routes: AppRouteObject[] = [
  {
    path: '/',
    element: <SidebarLayout />,
    children: [
      {
        index: true,
        handle: {
          crumb: 'Dashboard',
        },
        element: <HomePage />,
      },
      {
        path: 'users',
        handle: {
          crumb: 'List users',
        },
        element: <UsersPage />,

        children: [
          {
            path: ':userUUID',
            handle: {
              sidebarPath: 'users',
              crumb: ({ userUUID }: { userUUID: string }) => `User #${userUUID}`,
            },
            loader: ({ params }) => ({ userUUID: params.userUUID }),
            element: <UserDetailsPage />,
          },
          {
            path: 'new',
            handle: {
              crumb: 'New User',
            },
            element: <UsersNewPage />,
          },
        ],
      },
    ],
  },
]
