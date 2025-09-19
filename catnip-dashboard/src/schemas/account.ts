import { z } from 'zod'

export const accountSchema = z.object({
  uuid: z.uuid(),
  userUuid: z.uuid(),
  label: z.string(),
  balance: z.string().transform((str) => +str),
  createdAt: z.string().pipe(z.coerce.date()),
  updatedAt: z.string().pipe(z.coerce.date()),
})
export type Account = z.infer<typeof accountSchema>
