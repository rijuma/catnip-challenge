import { useLoaderData } from 'react-router-dom'

type UserDetailsPageProps = {
  userUUID: string
}

function UserDetailsPage() {
  const { userUUID }: UserDetailsPageProps = useLoaderData()

  return <div>User details: {userUUID}</div>
}

export default UserDetailsPage
