import { z } from 'zod'

export const createUserSchema = z.object({
  email: z.email(),
  firstName: z.string().max(255),
  lastName: z.string().max(255),
  phone: z.string().max(255).optional(),
  address: z.string().max(255).optional(),
})
export type CreateUser = z.infer<typeof createUserSchema>

export const updateUserSchema = createUserSchema.partial()
export type UpdateUser = z.infer<typeof updateUserSchema>

export const userSchema = z.object({
  uuid: z.uuid(),
  email: z.email(),
  firstName: z.string().max(255),
  lastName: z.string().max(255),
  phone: z.string().max(255).optional(),
  address: z.string().max(255).optional(),
  created_at: z.date(),
  updated_at: z.date(),
})
export type User = z.infer<typeof userSchema>
