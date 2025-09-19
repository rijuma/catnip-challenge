import { api } from '@/api/client'
import { useEffect, useState } from 'react'
import { toast } from 'sonner'
import type { z, ZodObject } from 'zod'

export type useApiResourceProps<Z extends ZodObject> = {
  url: string
  schema: Z
}
export const useApiResource = <Z extends ZodObject>({ url, schema }: useApiResourceProps<Z>) => {
  const [loading, setLoading] = useState(true)

  const [element, setElement] = useState<any>()

  const fetchElement = async (signal: AbortSignal) => {
    // Otherwise, do search
    try {
      setLoading(true)
      const response = await api.get(url, schema, {
        requestInit: { signal },
      })

      if (!response) throw new Error('No response from server.')

      setElement(response)
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

    fetchElement(signal)

    return () => {
      controller.abort('effect')
    }
  }, [url])

  return {
    loading,
    element: element as z.infer<Z>,
  }
}
