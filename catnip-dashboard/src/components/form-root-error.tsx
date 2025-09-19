import { AlertCircleIcon, CheckCircle2Icon, PopcornIcon } from 'lucide-react'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import type { FC } from 'react'
import type { FieldValues } from 'react-hook-form'

export type Props = {
  form: FieldValues
}

export const FormRootError: FC<Props> = ({ form }) => {
  const rootError = form.formState?.errors?.root?.message

  if (!rootError) return null

  return (
    <Alert variant="destructive">
      <AlertCircleIcon />
      <AlertTitle>Error processing the form.</AlertTitle>
      <AlertDescription>
        <p>{rootError}</p>
      </AlertDescription>
    </Alert>
  )
}
