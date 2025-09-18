// src/App.jsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import MainLayout from '@/layouts/main-layout'
import HomePage from '@/pages/home-page'
import UsersPage from '@/pages/users-page'
import UsersNewPage from '@/pages/users-new-page'

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'users', element: <UsersPage /> },
      { path: 'users/new', element: <UsersNewPage /> },
    ],
  },
])

function App() {
  return <RouterProvider router={router} />
}

export default App
