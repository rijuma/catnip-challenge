import { PaginatedTable, type TableColumns, type TableRows } from '@/components/paginated-table'
import { SearchField } from '@/components/search-field'
import { Section } from '@/components/section'
import { useApiList } from '@/hooks/use-api-list'
import { userSchema } from '@/schemas'
import { useState, type ComponentProps, type FC } from 'react'
import { useNavigate } from 'react-router-dom'

const columns: TableColumns = {
  email: {
    label: 'Email',
  },
  fullName: {
    label: 'Full Name',
  },
  createdAt: {
    label: 'Created At',
  },
}

type UsersListTableProps = {
  search: string
  onRowClick: ComponentProps<typeof PaginatedTable>['onRowClick']
}
const UsersListTable: FC<UsersListTableProps> = ({ search, onRowClick }) => {
  const [page, setPage] = useState(0)

  const { loading, list, count } = useApiList({
    search,
    url: '/users/',
    page,
    schema: userSchema,
  })

  const formatter = new Intl.DateTimeFormat('en-US', { dateStyle: 'short' })

  const rows: TableRows = list.map((user) => ({
    key: user.uuid,
    data: {
      uuid: user.uuid,
      email: user.email,
      fullName: [user.firstName, user.lastName].join(' '),
      createdAt: formatter.format(user.createdAt),
    },
  }))

  const handlePageChange = (page: number) => setPage(page)

  return rows.length ? (
    <div className={loading ? 'loading' : undefined}>
      <div className="text-sm mb-2 text-muted-foreground italic">
        {`Showing ${rows.length} of ${count} ${search !== '*' ? ` for "${search}"` : ''}:`}
      </div>
      <PaginatedTable
        onRowClick={onRowClick}
        columns={columns}
        rows={rows}
        pagination={{ currentPage: page, totalRows: count, onPageChange: handlePageChange }}
      />
    </div>
  ) : (
    <div className="text-center text-muted-foreground p-5 border-2 border-muted rounded-md ">
      No results for "{search}".
    </div>
  )
}

function UsersListPage() {
  const navigate = useNavigate()
  const [filter, updateFilter] = useState('')

  const handleUpdateFilter = (search: string) => {
    updateFilter(search)
  }

  const handleRowClick = (user: any) => {
    navigate(`/users/${user?.uuid}`)
  }

  return (
    <Section>
      <div>
        <SearchField autoFocus onDebouncedChange={handleUpdateFilter} />
      </div>
      {filter ? <UsersListTable search={filter} onRowClick={handleRowClick} /> : null}
    </Section>
  )
}

export default UsersListPage
