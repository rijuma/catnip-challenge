import { z, type ZodType } from 'zod'

export function parsePayload<T, S extends ZodType>(payload: T, schema: S) {
  const data = schema.parse(payload) as z.infer<S>

  return data
}
