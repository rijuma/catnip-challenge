import { PaginatedTable, type TableColumns, type TableRows } from '@/components/paginated-table'
import { SearchField } from '@/components/search-field'
import { Section } from '@/components/section'
import { useUsers } from '@/hooks'
import { useState } from 'react'
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

function UsersListPage() {
  const navigate = useNavigate()
  const [filter, updateFilter] = useState('')
  const [page, setPage] = useState(0)

  const { loading, userList, count } = useUsers({
    search: filter,
    page,
  })

  const handleUpdateFilter = (search: string) => {
    updateFilter(search)
  }

  const handleRowClick = (user: any) => {
    navigate(`/users/${user?.uuid}`)
  }

  const handlePageChange = (page: number) => setPage(page)

  const formatter = new Intl.DateTimeFormat('en-US', { dateStyle: 'short' })

  const rows: TableRows = userList.map((user) => ({
    key: user.uuid,
    data: {
      uuid: user.uuid,
      email: user.email,
      fullName: [user.firstName, user.lastName].join(' '),
      createdAt: formatter.format(user.createdAt),
    },
  }))

  return (
    <Section>
      <div>
        <SearchField autoFocus onDebouncedChange={handleUpdateFilter} />
      </div>
      {rows.length ? (
        <div className={loading ? 'loading' : undefined}>
          <PaginatedTable
            onRowClick={handleRowClick}
            columns={columns}
            rows={rows}
            pagination={{ currentPage: page, totalRows: count, onPageChange: handlePageChange }}
          />
        </div>
      ) : null}
    </Section>
  )
}

export default UsersListPage
