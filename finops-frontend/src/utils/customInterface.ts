export interface breadcrumbIteam {
    title: string
    disabled: boolean
  }
  
  export interface dataTableHeaders {
    title: string
    align: string
    key: string
  }
  
  export interface orphanResourcesData {
    cost: number
    location: string
    resource_group: string
    resource_id: string
    resource_name: string
    resource_type: string
  }
  
  export interface UntaggedResourceData {
    resource_type: string
    service: string
    region: string
    resource_name_or_id: string
    resource_arn: string
  }
  export interface carouselItem {
    title: string
    content: string
    progress: string
    image: string
  }
  
  export interface advisorRecommendation {
    category: string
    impact: string
    impacted_field: string
    problem: string
    recommendation_id: string
    resource_id: string
    resource_group: string
    solution: string
    source: null
    monthly_cost_savings: number
    recommendation: string
    resource: string
    savings_currency: string
  }