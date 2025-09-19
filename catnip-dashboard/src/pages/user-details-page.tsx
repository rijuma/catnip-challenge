import { Section } from '@/components/section'
import { useLoaderData } from 'react-router-dom'

type UserDetailsPageProps = {
  userUUID: string
}

function UserDetailsPage() {
  const { userUUID }: UserDetailsPageProps = useLoaderData()

  return (
    <Section>
      <h1>User details</h1>

      <pre>UUID: {userUUID}</pre>
    </Section>
  )
}

export default UserDetailsPage
