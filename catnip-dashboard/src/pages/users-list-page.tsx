import { PaginatedTable, type TableColumns, type TableRows } from '@/components/paginated-table'
import { SearchField } from '@/components/search-field'
import { Section } from '@/components/section'

const columns: TableColumns = {
  invoice: {
    label: 'Invoice',
  },
  paymentStatus: {
    label: 'Invoice',
  },
  paymentMethod: {
    label: 'Payment Method',
  },
  amount: {
    label: 'Amount',
    columnClassName: 'text-right',
  },
}

const rows: TableRows = [
  {
    key: 1,
    data: {
      invoice: 'INV001',
      paymentStatus: 'Paid',
      amount: '$250.00',
      paymentMethod: 'Credit Card',
    },
  },
  {
    key: 2,
    data: {
      invoice: 'INV002',
      paymentStatus: 'Pending',
      amount: '$150.00',
      paymentMethod: 'PayPal',
    },
  },
  {
    key: 3,
    data: {
      invoice: 'INV003',
      paymentStatus: 'Unpaid',
      amount: '$350.00',
      paymentMethod: 'Bank Transfer',
    },
  },
  {
    key: 4,
    data: {
      invoice: 'INV004',
      paymentStatus: 'Paid',
      amount: '$450.00',
      paymentMethod: 'Credit Card',
    },
  },
  {
    key: 5,
    data: {
      invoice: 'INV005',
      paymentStatus: 'Paid',
      amount: '$550.00',
      paymentMethod: 'PayPal',
    },
  },
  {
    key: 6,
    data: {
      invoice: 'INV006',
      paymentStatus: 'Pending',
      amount: '$200.00',
      paymentMethod: 'Bank Transfer',
    },
  },
  {
    key: 7,
    data: {
      invoice: 'INV007',
      paymentStatus: 'Unpaid',
      amount: '$300.00',
      paymentMethod: 'Credit Card',
    },
  },
]

function UsersListPage() {
  return (
    <Section>
      <div>
        <SearchField autoFocus />
      </div>
      <PaginatedTable columns={columns} rows={rows} />
    </Section>
  )
}

export default UsersListPage
