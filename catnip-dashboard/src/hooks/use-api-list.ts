import { api } from '@/api/client'
import { wrapWithPagination } from '@/schemas'
import { useRowsPerPageStore } from '@/stores'
import { useEffect, useState } from 'react'
import { toast } from 'sonner'
import type { z, ZodObject } from 'zod'

const listInit = {
  items: [],
  count: 0,
}

export type useApiListFilters<Z extends ZodObject> = {
  url: string
  schema: Z
  search?: string
  page?: number
}
export const useApiList = <Z extends ZodObject>({
  search,
  page = 0,
  url,
  schema,
}: useApiListFilters<Z>) => {
  const [loading, setLoading] = useState(true)
  const [rowsPerPage] = useRowsPerPageStore()

  const [listState, setListState] = useState<{
    items: unknown[]
    count: number
  }>(listInit)
  const filters: string[] = []

  if (search && search !== '*') filters.push(`q=${encodeURIComponent(search)}`)

  if (page) filters.push(`offset=${(page - 1) * rowsPerPage}`)

  filters.push(`limit=${rowsPerPage}`)

  const urlFilters = filters.join('&')

  const fetchUsers = async (signal: AbortSignal) => {
    // If nothing to search, clear
    if (!search) {
      setListState(listInit)
      return
    }

    // Otherwise, do search
    try {
      setLoading(true)
      const response = await api.get(`${url}?${urlFilters}`, wrapWithPagination(schema), {
        requestInit: { signal },
      })

      if (!response) throw new Error('No response from server.')

      setListState({ ...response })
    } catch (e) {
      if (e === 'effect') return // Just the useEffect reloading.

      toast('Error fetching API', {
        description: 'There was an error fetching the API. Please try again in a minute.',
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
    list: listState.items as z.infer<Z>[],
    count: listState.count,
  }
}
