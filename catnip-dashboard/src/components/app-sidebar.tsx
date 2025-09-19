import { Link } from 'react-router'
import { useLocation } from 'react-router-dom'
import { Cat } from 'lucide-react'
import { NavUser } from './nav-user'
import type { ComponentProps, FC } from 'react'

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from '@/components/ui/sidebar'

const data = {
  user: {
    name: 'Admin',
    email: 'admin@catnip-bank.com',
    avatar: 'https://randomuser.me/api/portraits/lego/7.jpg',
  },
  navMain: [
    {
      title: 'Home',
      items: [
        {
          title: 'Dashboard',
          to: { pathname: '/' },
        },
      ],
    },
    {
      title: 'Users',
      items: [
        {
          title: 'New user',
          to: { pathname: '/users/new' },
        },
        {
          title: 'List users',
          to: { pathname: '/users' },
        },
      ],
    },
  ],
}

export const AppSidebar: FC<ComponentProps<typeof Sidebar>> = ({ ...props }) => {
  const location = useLocation()
  const currentPathname = location.pathname

  return (
    <Sidebar {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <Link to={{ pathname: '/' }}>
                <div className="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg">
                  <Cat className="size-4" />
                </div>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-medium">Meownybags Dashboard</span>
                  <span className="">v0.0.1</span>
                </div>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        {data.navMain.map((item) => (
          <SidebarGroup key={item.title}>
            <SidebarGroupLabel>{item.title}</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {item.items.map(({ title, to }) => (
                  <SidebarMenuItem key={title}>
                    <SidebarMenuButton asChild isActive={currentPathname === to.pathname}>
                      <Link to={to}>{title}</Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
