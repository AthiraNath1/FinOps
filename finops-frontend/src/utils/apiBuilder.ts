import axios from 'axios'
import type { AxiosResponse } from 'axios'

export const getRequest = (url: string): Promise<AxiosResponse> => {
   
        const token = localStorage.getItem('token');

  return axios.get(url, {
    headers: { 'Access-Control-Allow-Origin': '*',
      'Authorization': `Bearer ${token}` 
     },
    withCredentials: true
  })
}

export const getRequestWithData = (url: string, data: any): Promise<AxiosResponse> => {
  const token = localStorage.getItem('token');

  return axios.get(url, { params: data,
    headers: {
      Authorization: `Bearer ${token}`,
    },
   })
}

export const postRequest = (url: string, data: any): Promise<AxiosResponse> => {
  const token = localStorage.getItem('token');
  
  return axios.post(url, data, {
    withCredentials: true,
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
}

export const filePostRequest = (url: string, data: any): Promise<AxiosResponse> => {
  return axios.post(url, data)
}

export const putRequest = (url: string, data: any): Promise<AxiosResponse> => {
  return axios.put(url, data)
}

export const putRequestWithData = (url: string, data: any): Promise<AxiosResponse> => {
  return axios.put(url, data, { params: data })
}

export const deleteRequest = (url: string, data: any): Promise<AxiosResponse> => {
  const token = localStorage.getItem('token');
  return axios.delete(url, {
    data: data,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });}

export const deleteRequestwithParams = (url: string): Promise<AxiosResponse> => {
  const token = localStorage.getItem('token');

  return axios.delete(url, {
    headers: { 'Access-Control-Allow-Origin': '*' ,
      'Authorization': `Bearer ${token}` 
    },
    withCredentials: true
  })
}

export const postRequestWithHeaders = (
  url: string,
  data: any,
  headers: any
): Promise<AxiosResponse> => {
  return axios.post(url, data, {
    headers: {
      ...headers
    },
    withCredentials: true
  })
}