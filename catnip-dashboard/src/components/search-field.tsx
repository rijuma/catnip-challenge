import { Command, CommandInput, type CommandInputProps } from '@/components/ui/command'
import { cn, type ClassName } from '@/lib/utils'
import { useEffect, useRef, useState, type FC, type KeyboardEvent } from 'react'

export type Props = CommandInputProps & {
  onChange?: (search: string) => {}
  onDebouncedChange?: (search: string) => {}
  className?: ClassName
}

export const SearchField: FC<Props> = ({
  className,
  onChange,
  onDebouncedChange,
  ...inputProps
}) => {
  const [value, setValue] = useState('')
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    const handler = setTimeout(() => {
      onDebouncedChange?.(value)
      // Perform your search/API call here using 'searchTerm'
    }, 500) // 500ms delay

    return () => {
      clearTimeout(handler)
    }
  }, [value]) // Re-run effect when searchTerm changes

  const clearInput = () => {
    setValue('')
    onDebouncedChange?.('')
    inputRef?.current?.focus()
  }

  const handleChange = (search: string) => {
    setValue(search)
    onChange?.(search)
  }

  const handleClear = () => clearInput()

  const handleKeyDown = ({ key }: KeyboardEvent) => {
    if (key === 'Escape') clearInput()
  }

  return (
    <div
      className={cn('mx-auto flex w-full max-w-2xl min-w-0 flex-1 flex-col px-4 py-6', className)}
    >
      <Command>
        <CommandInput
          ref={inputRef}
          value={value}
          onValueChange={handleChange}
          placeholder="Search users..."
          onKeyDown={handleKeyDown}
          onClear={value ? handleClear : undefined}
          {...inputProps}
        />
      </Command>
      <div className="px-4 py-1 text-xs text-muted-foreground italic text-right">
        * = list all users
      </div>
    </div>
  )
}
