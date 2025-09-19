import { api } from '@/api/client'
import { wrapWithPagination, userSchema, type User } from '@/schemas'
import { useRowsPerPageStore } from '@/stores'
import { useEffect, useState } from 'react'
import { toast } from 'sonner'

export type UseUsersFilters = {
  search?: string
  page?: number
}
export const useUsers = ({ search, page = 0 }: UseUsersFilters) => {
  const [loading, setLoading] = useState(true)
  const [rowsPerPage] = useRowsPerPageStore()

  const [userList, setUserList] = useState<User[]>([])
  const [count, setCount] = useState(0)

  const filters: string[] = []

  if (search && search !== '*') filters.push(`q=${encodeURIComponent(search)}`)

  if (page) filters.push(`offset=${(page - 1) * rowsPerPage}`)

  filters.push(`limit=${rowsPerPage}`)

  const urlFilters = filters.join('&')

  const fetchUsers = async (signal: AbortSignal) => {
    // If nothing to search, clear
    if (!search) {
      setUserList([])
      setCount(0)
      return
    }

    // Otherwise, do search
    try {
      setLoading(true)
      const response = await api.get(`/users?${urlFilters}`, wrapWithPagination(userSchema), {
        requestInit: { signal },
      })

      if (!response) throw new Error('No response from server.')

      setUserList(response.items)
      setCount(response.count)
    } catch (e) {
      if (e === 'effect') return // Just the useEffect reloading.
      toast('Error fetching users', {
        description: 'There was an error fetching the users. Please try again in a minute.',
      })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const controller = new AbortController()
    const { signal } = controller

    fetchUsers(signal)

    return () => {
      controller.abort('effect')
    }
  }, [search, rowsPerPage, page])

  return {
    loading,
    userList,
    count,
  }
}
