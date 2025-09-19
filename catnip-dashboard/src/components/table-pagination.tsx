import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Pagination, PaginationContent, PaginationItem } from '@/components/ui/pagination'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { rowsPerPageDefault, rowsPerPageOptions } from '@/const/tables'
import { ChevronLeftIcon, ChevronRightIcon } from 'lucide-react'
import { type FC } from 'react'

export type Props = {
  currentPage?: number
  totalRows: number
  rowsPerPage?: number
  onRowsPerPageChange: (count: number) => void
  onPageChange: (page: number) => void
}

export const TablePagination: FC<Props> = ({
  currentPage = 1,
  totalRows,
  rowsPerPage = rowsPerPageDefault,
  onRowsPerPageChange,
  onPageChange,
}) => {
  if (totalRows <= rowsPerPage) return null

  return (
    <div className="w-full flex items-center justify-between gap-2">
      <div className="flex items-center gap-2">
        <Label className="whitespace-nowrap">Rows per page:</Label>
        <Select
          value={rowsPerPage.toString()}
          onValueChange={(rowsPerPage) => onRowsPerPageChange(+rowsPerPage)}
        >
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {rowsPerPageOptions.map((count) => (
              <SelectItem key={count} value={`${count}`}>
                {count}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-sm text-muted-foreground whitespace-nowrap">
          {(currentPage - 1) * rowsPerPage + 1}-{currentPage * rowsPerPage} of {totalRows}
        </span>
        <Pagination>
          <PaginationContent>
            <PaginationItem>
              <Button
                aria-label="Previous page"
                size="icon"
                variant="ghost"
                disabled={currentPage === 1}
                onClick={() => onPageChange(currentPage - 1)}
              >
                <ChevronLeftIcon className="h-4 w-4" />
              </Button>
            </PaginationItem>
            <PaginationItem>
              <Button
                aria-label="Next page"
                size="icon"
                variant="ghost"
                disabled={currentPage * rowsPerPage >= totalRows}
                onClick={() => onPageChange(currentPage + 1)}
              >
                <ChevronRightIcon className="h-4 w-4" />
              </Button>
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  )
}
