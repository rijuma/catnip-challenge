import { z, type ZodObject } from 'zod'

export function parsePayload<T, S extends ZodObject>(payload: T, schema: S) {
  const data = schema.parse(payload) as z.infer<S>

  return data
}

export function wrapWithPagination<T extends ZodObject>(schema: T) {
  return z.object({
    items: z.array(schema),
    count: z.number(),
  })
}
