// src/App.jsx
import SidebarLayout from '@/layouts/sidebar-layout'
import HomePage from '@/pages/home-page'
import UsersListPage from '@/pages/users-lists-page'
import UserDetailsPage from '@/pages/user-details-page'
import UsersNewPage from '@/pages/users-new-page'
import type { AppRouteObject } from '@/types'
import { Outlet } from 'react-router-dom'

const NoLayout = <Outlet /> // Just an utility class to group URLs without a Layout

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
        element: NoLayout,
        children: [
          {
            index: true,
            handle: {
              crumb: 'List users',
            },
            element: <UsersListPage />,
          },
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
