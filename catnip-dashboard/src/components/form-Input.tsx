import type { ComponentProps, FC } from 'react'
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from './ui/form'
import { Input } from './ui/input'
import { cn, type ClassName } from '@/lib/utils'

export type Props = Omit<ComponentProps<typeof FormField>, 'render'> & {
  className: ClassName
  label: string
  placeholder?: string
  description?: string
  type?: HTMLInputElement['type']
}
export const FormInput: FC<Props> = ({
  placeholder,
  className,
  label,
  description,
  type,
  ...formFieldProps
}) => (
  <div className={cn(className)}>
    <FormField
      {...formFieldProps}
      render={({ field }) => (
        <FormItem>
          <FormLabel>{label}</FormLabel>
          <FormControl>
            <Input type={type} placeholder={placeholder} {...field} />
          </FormControl>
          {description ? <FormDescription>{description}</FormDescription> : null}
          <FormMessage />
        </FormItem>
      )}
    />
  </div>
)
