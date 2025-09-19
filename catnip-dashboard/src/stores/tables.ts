import { atom } from 'nanostores'
import { useStore } from '@nanostores/react'

const $rowsPerPage = atom<number | undefined>()

export const useRowsPerPageStore = () => {
  const rowsPerPage = useStore($rowsPerPage)
  const setRowsPerPage = (value: number) => $rowsPerPage.set(value)

  return [rowsPerPage, setRowsPerPage] as const
}
