import { apiUrl } from '@/const'
import { objectToSnake, objectToCamel } from 'ts-case-convert'
import { parsePayload } from '../schemas/_utils'
import { ApiError } from './error'
import type { ZodObject } from 'zod'
import type { ApiCallOptions } from '@/types/api'

const fetchApi = async <T extends ZodObject, P extends Object>(
  method: string,
  path: string,
  schema?: T,
  body?: P,
  options?: RequestInit,
  extraHeaders?: RequestInit['headers'],
) => {
  const headers: HeadersInit = new Headers({
    Accept: 'application/json',
    // 'X-API-Key': API_KEY ,
    ...extraHeaders,
  })

  let bodyPayload: any

  if (body) {
    // If there's a body we add the proper header.
    const isFormData = body instanceof FormData
    if (!isFormData) headers.set('Content-Type', 'application/json')
    bodyPayload = isFormData ? body : JSON.stringify(objectToSnake(body))
  }

  const requestInit = {
    method,
    headers,
    ...options,
    body: bodyPayload,
  } satisfies RequestInit

  const url = `${apiUrl}${path}`

  const response = await fetch(url, requestInit)

  let payload
  try {
    payload = await response.json()
  } catch (e) {
    // Empty or not json.
  }

  if (!response.ok || response.status >= 400)
    throw new ApiError({
      message: response.statusText || payload?.message || `Error ${response.status}`,
      status: response.status,
      response,
      payload,
    })

  if (!schema) return

  try {
    const data = parsePayload(objectToCamel(payload), schema)

    return data
  } catch (e) {
    console.error(
      `Invalid API response [${requestInit.method.toUpperCase()}] ${url}:`,
      payload,
      'Details: ',
      (e as Error).message,
    )

    throw new ApiError({
      message: 'Invalid API response.',
      response,
      payload,
    })
  }
}

const apiCall = async <T extends ZodObject, P extends Object>(
  method: string,
  path: string,
  schema?: T,
  { body, requestInit, extraHeaders }: ApiCallOptions<P> = {},
) => {
  // First attempt
  const response = await fetchApi(method, path, schema, body, requestInit, extraHeaders)

  return response
}

export const api = {
  get: <T extends ZodObject, P extends Object>(
    path: string,
    schema: T,
    options?: ApiCallOptions<P>,
  ) => apiCall('GET', path, schema, options),
  post: <T extends ZodObject, P extends Object>(
    path: string,
    schema?: T,
    options?: ApiCallOptions<P>,
  ) => apiCall('POST', path, schema, options),
  put: <T extends ZodObject, P extends Object>(
    path: string,
    schema?: T,
    options?: ApiCallOptions<P>,
  ) => apiCall('PUT', path, schema, options),
  patch: <T extends ZodObject, P extends Object>(
    path: string,
    schema?: T,
    options?: ApiCallOptions<P>,
  ) => apiCall('PATCH', path, schema, options),
  delete: <T extends ZodObject, P extends Object>(
    path: string,
    schema?: T,
    options?: ApiCallOptions<P>,
  ) => apiCall('DELETE', path, schema, options),
}
