import { Toaster } from '@/components/ui/sonner'

import { Outlet } from 'react-router-dom'
export default function RootLayout() {
  return (
    <>
      <Outlet />
      <Toaster />
    </>
  )
}
