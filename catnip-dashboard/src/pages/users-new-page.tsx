import { EditUserForm } from '@/components/create-user-form'
import { Section } from '@/components/section'
import type { User } from '@/schemas'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'

function UsersNewPage() {
  const navigate = useNavigate()

  const handleSuccess = (user: User) => {
    toast('User has been created', {
      action: {
        label: 'Open',
        onClick: () => navigate(`/users/${user.uuid}`),
      },
    })

    navigate('/users/')
  }

  return (
    <Section>
      <EditUserForm onCancel={() => navigate('/users/')} onSuccess={handleSuccess} />
    </Section>
  )
}

export default UsersNewPage
