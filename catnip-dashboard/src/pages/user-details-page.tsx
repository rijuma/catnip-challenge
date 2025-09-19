import { PaginatedTable, type TableColumns, type TableRows } from '@/components/paginated-table'
import { Section } from '@/components/section'
import { useApiList, useApiResource } from '@/hooks'
import { accountSchema, userSchema } from '@/schemas'
import { useLoaderData } from 'react-router-dom'

const columns: TableColumns = {
  uuid: {
    label: 'UUID',
  },
  label: {
    label: 'Label',
  },
  balance: {
    label: 'Label',
    columnClassName: 'text-right',
  },
}

type UserDetailsPageProps = {
  userUUID: string
}

function UserDetailsPage() {
  const { userUUID }: UserDetailsPageProps = useLoaderData()

  const { loading: loadingUser, element: user } = useApiResource({
    url: `/users/${userUUID}`,
    schema: userSchema,
  })
  const { loading: loadingAccounts, list: accounts } = useApiList({
    url: `/users/${userUUID}/accounts`,
    schema: accountSchema,
  })

  const formatter = new Intl.DateTimeFormat('en-US', { dateStyle: 'short' })

  console.log({ accounts })

  const rows: TableRows = accounts.map((account) => ({
    key: account.uuid,
    data: {
      uuid: account.uuid,
      label: account.label,
      balance: account.balance,
      createdAt: formatter.format(account.createdAt),
      updatedAt: formatter.format(account.updatedAt),
    },
  }))

  return (
    <Section>
      <h1>User details</h1>

      <pre>{JSON.stringify(user, null, 2)}</pre>
      <hr />
      <h2>User Accounts</h2>
      {rows.length ? (
        <PaginatedTable columns={columns} rows={rows} />
      ) : (
        <div className="text-center text-muted-foreground p-5 border-2 border-muted rounded-md ">
          This user has no accounts at the moment.
        </div>
      )}
    </Section>
  )
}

export default UserDetailsPage
