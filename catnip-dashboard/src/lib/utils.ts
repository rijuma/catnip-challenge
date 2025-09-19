import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export type ClassName = ClassValue[]

export function cn(...inputs: ClassName) {
  return twMerge(clsx(inputs))
}
