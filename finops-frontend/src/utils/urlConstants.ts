const BASE_URL = "http://localhost:8000";


// USER LOGIN API
const USERLOGIN = BASE_URL + '/login'

const INTROSPECT = BASE_URL + '/introspect'

const LOGOUT = BASE_URL + '/logout'

const LIST = BASE_URL + '/list'


// Register user in Azure
const SIGNINAZURELOGIN = BASE_URL + '/azure/signup'

// Orphan Resources
//  Azure --
const AZURESUBCRIPTIONLIST = BASE_URL + '/azure/subscription_list'

const AZUREORPHANRESOURCES = BASE_URL + '/azure/orphan_resources'

const DELETEORPHANRESOURCES = BASE_URL + '/azure/delete_orphan_resources'


//Underutilized Resources
const UTILIZEDRESOURCES = BASE_URL + '/azure/underutilizedresources'

// Advisor Recommendation
const ADVISOR = BASE_URL + '/azure/advisor'

const ADVISORACTIVEDATA = BASE_URL + '/active_data'

const ADVISORIGNOREDATA = BASE_URL + '/ignore_data'

const EXCLUDERECOMMENDATIONS = BASE_URL + '/exclude_recommendations'

const INCLUDERECOMMENDATIONS = BASE_URL + '/include_recommendations'

// AKS Resources
const AKSRESOURCES = BASE_URL + '/azure/all_aks'

const STARTAKSRESOURCES = BASE_URL + '/azure/start_aks'

const STOPAKSRESOURCES = BASE_URL + '/azure/start_aks'

// Resources Open to Public
const PUBLICRESOURCES = BASE_URL + '/network_properties'

//Untagged Resources

const AZUREUNTAGGEDRESOURCES = BASE_URL + '/azure/untagged_resources'


const AZURETAGRESOURCES = BASE_URL + '/azure/tag_resources'


const AZUREFINXRECOMMENDATION = BASE_URL + '/finx-recommendation/azure/finx-recommendations'

const SINGUP = BASE_URL + '/create'

const JIRAPROJECTS = BASE_URL + '/issue-creation/get_all_jira_projects'

const INTEGRATEJIRA = BASE_URL + '/issue-creation/integrate_jira'

const CREATEJIRA = BASE_URL + '/issue-creation/create_client_jira_issue'

export {
  BASE_URL,
  USERLOGIN,
  INTROSPECT,
  LOGOUT,
  LIST,
  SIGNINAZURELOGIN,
  AZURESUBCRIPTIONLIST,
  AZUREORPHANRESOURCES,
  DELETEORPHANRESOURCES,
  UTILIZEDRESOURCES,
  ADVISOR,
  ADVISORACTIVEDATA,
  ADVISORIGNOREDATA,
  EXCLUDERECOMMENDATIONS,
  INCLUDERECOMMENDATIONS,
  AKSRESOURCES,
  STARTAKSRESOURCES,
  STOPAKSRESOURCES,
  PUBLICRESOURCES,
  AZUREUNTAGGEDRESOURCES,
  AZURETAGRESOURCES,
  AZUREFINXRECOMMENDATION,
  SINGUP,
  JIRAPROJECTS,
  INTEGRATEJIRA,
  CREATEJIRA
}