import * as APIBuilder from '../apiBuilder'
import * as URLConstants from '../urlConstants'
import axios from 'axios'

export const Login = (data: any) => {
  return APIBuilder.postRequest(URLConstants.USERLOGIN, data)
}

export const login = (data: any) => {

  return axios.post(URLConstants.USERLOGIN, data, {
    withCredentials: true
  })

}

export const introspect = () => {
  return APIBuilder.getRequest(URLConstants.INTROSPECT)
}

export const logout = () => {
  return APIBuilder.getRequest(URLConstants.LOGOUT)
}

export const serviceList = (service: string) => {
  return APIBuilder.getRequest(URLConstants.LIST + '?platform=' + service)
}

export const getSubscribersList = (data: any) => {
  return APIBuilder.getRequest(
    URLConstants.AZURESUBCRIPTIONLIST + '?integration_name=' + data.integration_name
  )
}

export const getOrphanResources = (data: any) => {
  return APIBuilder.getRequest(
    URLConstants.AZUREORPHANRESOURCES +
      '?integration_name=' +
      data.integration_name +
      '&subscription_id=' +
      data.subscription_id
  )
}

export const deleteOrphanResources = (data: any) => {
  return APIBuilder.deleteRequest(URLConstants.DELETEORPHANRESOURCES, { data })
}

export const getUtilizedResources = (data: any) => {
  return APIBuilder.getRequest(
    URLConstants.UTILIZEDRESOURCES +
      '?integration_name=' +
      data.integration_name +
      '&subscription_id=' +
      data.subscription_id
  )
}

export const getAdvisor = (data: any) => {
  return APIBuilder.getRequest(
    URLConstants.ADVISOR +
      '?integration_name=' +
      data.integration_name +
      '&subscription_id=' +
      data.subscription_id
  )
}

//Azure Advisor
export const getAdvisorActiveData = (data: any) => {
  return APIBuilder.getRequest(
    URLConstants.ADVISORACTIVEDATA +
      '?integration_name=' +
      data.integration_name +
      '&subscription_id=' +
      data.subscription_id
  )
}

export const getAdvisorIgnoreData = (data: any) => {
  return APIBuilder.getRequest(
    URLConstants.ADVISORIGNOREDATA +
      '?integration_name=' +
      data.integration_name +
      '&subscription_id=' +
      data.subscription_id
  )
}



export const excludeRecommendations = (data: any) => {
  return APIBuilder.postRequest(
    URLConstants.EXCLUDERECOMMENDATIONS + '?integration_name=' + data.integration_name,
    { recommendation_id: data.recommendation_id }
  )
}

export const includeRecommendations = (data: any) => {
  return APIBuilder.postRequest(
    URLConstants.INCLUDERECOMMENDATIONS + '?integration_name=' + data.integration_name,
    { recommendation_id: data.recommendation_id }
  )
}

export const getAksResources = (data: any) => {
  return APIBuilder.getRequestWithData(URLConstants.AKSRESOURCES, data)
}

export const startAksResources = (data: any) => {
  return APIBuilder.postRequest(URLConstants.STARTAKSRESOURCES, data)
}

export const stoptAksResources = (data: any) => {
  return APIBuilder.postRequest(URLConstants.STOPAKSRESOURCES, data)
}

export const getPublicResources = (data: any) => {
  return APIBuilder.getRequest(
    URLConstants.PUBLICRESOURCES +
      '?integration_name=' +
      data.integration_name +
      '&subscription_id=' +
      data.subscription_id
  )
}

export const signUp = (data: any) => {
  return axios.post(URLConstants.SINGUP, data, {
    withCredentials: true
  })
}


export const getAzureUntaggedResources = (data: any) => {
  return APIBuilder.getRequest(
    URLConstants.AZUREUNTAGGEDRESOURCES +
      '?integration_name=' +
      data.integration_name +
      '&subscription_id=' +
      data.subscription_id
  )
}

export const postTagsToAzureResources = (data: any, value: any) => {
  return APIBuilder.postRequest(
    URLConstants.AZURETAGRESOURCES +
      '?integration_name=' +
      data.integration_name +
      '&subscription_id=' +
      data.subscription_id +
      '&resource_id=' +
      data.resource_id,
    value
  )
}

export const getAzureFinXRecommendation = (data: any) => {
  return APIBuilder.getRequest(
    URLConstants.AZUREFINXRECOMMENDATION +
      '?integration_name=' +
      data.integration_name +
      '&subscription_id=' +
      data.subscription_id
  )
}

export const getAllJiraProjects = (data: any) => {
  return APIBuilder.getRequest(
    URLConstants.JIRAPROJECTS + '?integration_name=' + data.integration_name
  )
}

export const createJira = (data: any, headers: any) => {
  return APIBuilder.postRequestWithHeaders(URLConstants.INTEGRATEJIRA, data, headers)
}

export const createClientJiraIssue = (data: any) => {
  return APIBuilder.postRequest(
    URLConstants.CREATEJIRA + '?integration_name=' + data.integration_name,
    data
  )
}