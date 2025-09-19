export class ApiError extends Error {
  status?: number
  response?: Response
  payload?: Object

  constructor({
    message,
    status,
    response,
    payload,
  }: {
    message: string
    status?: number
    response?: Response
    payload?: Object
  }) {
    super(message)
    this.status = status
    this.response = response
    this.payload = payload
  }
}
