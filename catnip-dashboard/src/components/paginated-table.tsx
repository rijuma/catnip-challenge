import {
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { cn, type ClassName } from '@/lib/utils'
import { TablePagination } from './table-pagination'
import { useRowsPerPageStore } from '@/stores'
import type { FC } from 'react'

export type TableColumn = {
  label: string
  className?: ClassName
  columnClassName?: ClassName
}

export type TableColumns = Record<string, TableColumn>

export type TableRow = {
  key: string | number
  data: Record<string, string | number>
}

export type TableRows = TableRow[]

export type Props = {
  pagination?: {
    currentPage: number
    totalRows: number
    onPageChange: (page: number) => void
  }
  columns: TableColumns
  rows: TableRows
}

export const PaginatedTable: FC<Props> = ({ columns, rows, pagination }) => {
  const [rowsPerPage, setRowsPerPage] = useRowsPerPageStore()

  const columnMap = new Map(Object.entries(columns))

  return (
    <Table>
      <TableHeader>
        <TableRow>
          {Array.from(columnMap).map(([column, { label, className, columnClassName }]) => (
            <TableHead key={column} className={cn(className, columnClassName)}>
              {label}
            </TableHead>
          ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {rows.map(({ key, data }) => (
          <TableRow key={key}>
            {Array.from(columnMap).map(([column, columnData]) => {
              if (data[column] === undefined)
                console.warn(`PaginatedTable: Missing value for column ${column} on row`, data)

              const value = data[column] ?? ''

              const columnClassName = columnData.columnClassName

              return (
                <TableCell key={column} className={cn(columnClassName)}>
                  {value}
                </TableCell>
              )
            })}
          </TableRow>
        ))}
      </TableBody>
      {pagination !== undefined ? (
        <TableFooter>
          <TablePagination
            rowsPerPage={rowsPerPage}
            onRowsPerPageChange={(value) => setRowsPerPage(value)}
            {...pagination}
          />
        </TableFooter>
      ) : null}
    </Table>
  )
}
