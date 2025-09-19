import { zodResolver } from '@hookform/resolvers/zod'
import { createUserSchema, updateUserSchema, type CreateUser, type UpdateUser } from '@/schemas'
import { useForm } from 'react-hook-form'
import { FormInput } from './form-Input'
import { Form } from './ui/form'
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from './ui/button'
import { useState, type FC } from 'react'
import { api } from '@/api/client'

export type Props = {
  user?: CreateUser | UpdateUser
  onCancel?: () => void
  onSuccess?: () => void
}
export const EditUserForm: FC<Props> = ({ user, onCancel, onSuccess }) => {
  const [loading, setLoading] = useState(false)

  const form = useForm<CreateUser | UpdateUser>({
    resolver: zodResolver(user ? updateUserSchema : createUserSchema),
    defaultValues: {
      ...user,
    },
  })

  const onSubmit = async (values: CreateUser | UpdateUser) => {
    if (loading) return

    try {
      form.clearErrors()

      setLoading(true)

      const payload = await api.post(`/users`, createUserSchema)

      onSuccess?.()
    } catch (e) {
      form.setError('root', { message: `Error creating user: ${(e as Error).message}` })
    } finally {
      setLoading(false)
    }

    console.log(values)
    return false
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <Card className="w-full">
          <CardHeader>
            <CardTitle>Create user</CardTitle>
          </CardHeader>
          <CardContent className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <FormInput
              className="col-span-full"
              control={form.control}
              name="email"
              label="Email"
            />
            <FormInput
              className="col-span-1"
              control={form.control}
              name="firstName"
              label="First Name"
            />
            <FormInput
              className="col-span-1"
              control={form.control}
              name="lastName"
              label="Last Name"
            />
            <FormInput
              className="col-span-full"
              control={form.control}
              name="phone"
              label="Phone"
              type="tel"
            />
            <FormInput
              className="col-span-full"
              control={form.control}
              name="address"
              label="Address"
            />
          </CardContent>
          <hr />
          <CardFooter className="flex-col gap-4">
            <Button type="submit" className="w-full">
              Create
            </Button>
            {onCancel ? (
              <Button type="button" variant="outline" onClick={() => onCancel()} className="w-full">
                Cancel
              </Button>
            ) : null}
          </CardFooter>
        </Card>
      </form>
    </Form>
  )
}
