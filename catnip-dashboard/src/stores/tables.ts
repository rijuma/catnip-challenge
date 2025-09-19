import { atom } from 'nanostores'
import { useStore } from '@nanostores/react'
import { rowsPerPageDefault } from '@/const/tables'

const $rowsPerPage = atom<number>(rowsPerPageDefault)

export const useRowsPerPageStore = () => {
  const rowsPerPage = useStore($rowsPerPage)

  const setRowsPerPage = (value: number) => $rowsPerPage.set(value)

  return [rowsPerPage, setRowsPerPage] as const
}
