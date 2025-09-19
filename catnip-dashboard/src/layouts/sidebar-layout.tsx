import { SidebarProvider, SidebarTrigger, SidebarInset } from '@/components/ui/sidebar'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'
import { Separator } from '@/components/ui/separator'
import { AppSidebar } from '@/components/app-sidebar'
import { useAppMatches } from '@/hooks'

import { Outlet } from 'react-router-dom'
import { Fragment } from 'react/jsx-runtime'

export default function SidebarLayout() {
  const matches = useAppMatches()
  console.log({ matches })
  const crumbs = matches
    .filter((match) => Boolean(match.handle?.crumb))
    // map to an array of breadcrumb elements
    .map((match, idx) => {
      const crumb = match.handle.crumb
      const data = match.loaderData

      console.log({ crumb })

      // Handle dynamic crumbs that are functions
      const breadcrumbTitle = typeof crumb === 'function' ? crumb(data) : crumb

      return (
        <Fragment key={idx}>
          {idx !== 0 ? <BreadcrumbSeparator className="hidden md:block" /> : null}
          <BreadcrumbItem className="hidden md:block">
            <BreadcrumbLink to={{ pathname: match.pathname }}>{breadcrumbTitle}</BreadcrumbLink>
          </BreadcrumbItem>
        </Fragment>
      )
    })

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 data-[orientation=vertical]:h-4" />
          {crumbs.length ? (
            <Breadcrumb>
              <BreadcrumbList>{crumbs}</BreadcrumbList>
            </Breadcrumb>
          ) : null}
        </header>
        <main>
          <Outlet />
        </main>
      </SidebarInset>
    </SidebarProvider>
  )
}
