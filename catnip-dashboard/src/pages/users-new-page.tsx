import { EditUserForm } from '@/components/edit-user-form'
import { Section } from '@/components/section'
import { useNavigate } from 'react-router-dom'

function UsersNewPage() {
  const navigate = useNavigate()

  return (
    <Section>
      <EditUserForm onCancel={() => navigate('/users/')} />
    </Section>
  )
}

export default UsersNewPage
