import type { FC, PropsWithChildren } from 'react'
import { cn, type ClassName } from '@/lib/utils'

export type Props = PropsWithChildren<{
  className?: ClassName
}>

export const Section: FC<Props> = ({ className, children }) => (
  <div
    className={cn(
      'mx-auto flex w-full max-w-2xl min-w-0 flex-1 flex-col gap-8 px-4 py-6',
      className,
    )}
  >
    {children}
  </div>
)
