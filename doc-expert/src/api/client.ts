import type { AxiosRequestConfig } from "axios"
import Axios, { AxiosError } from "axios"

export const axiosInstance = Axios.create({
  baseURL: "http://localhost:8000",
  // baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 15 * 1000
})

type CustomAxiosProps = AxiosRequestConfig & {
  Authentication?: string
}

export const customAxios = <T>(config: CustomAxiosProps): Promise<T> => {
  // const headers = config?.Authentication
  //   ? {
  //       ...config?.headers,
  //       Authorization: `Bearer 7ff827f5f1d4e7ff61afe4bb2c3d031147e3bc9e`,
  //       // Cookie: `Authentication=${config?.Authentication || ''}`,
  //     }
  //   : config?.headers;

  const headers = {
    Authorization: `Bearer 7ff827f5f1d4e7ff61afe4bb2c3d031147e3bc9e`
  }
  return axiosInstance({
    ...config,
    headers
    // withCredentials: true,
  }).then((response) => response.data as T)
}

export class VisionError<T> extends AxiosError<T> {}

export interface ErrorType<Error> extends VisionError<Error> {}

// export type CustomErrorType = DeveloggerError<ApiResponse>;
