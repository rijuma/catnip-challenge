export type ApiCallOptions<P extends Object> = {
  body?: P
  requestInit?: RequestInit
  extraHeaders?: RequestInit['headers']
}
