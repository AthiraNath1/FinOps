<template>
    <div>
      <v-row justify="center">
        <v-dialog :model-value="dialog" persistent width="950">
          <v-card >
            <v-col cols="12" class="d-flex justify-end align-center">
                <v-icon start icon="mdi-close" color="#003156" size="large" @click="closeDialog"></v-icon>
            </v-col>
            
            <v-container class=" d-flex justify-center align-center">
                <v-col cols="11" class="main-content border scroll">
					<v-row>
						<v-col cols="3" class="border-right border-bottom">
							<p>Recommendation_ID</p> 
						</v-col>
						<v-col cols="9" class="border-bottom">
							<span>{{ item.recommendation_id }}</span>
						</v-col>
						<v-col cols="3" class="border-right border-bottom">
						<p>Impacted_Field</p> 
						</v-col>
						<v-col cols="9" class="border-bottom">
							<span>
								{{ item.impacted_field }}
							</span>
						</v-col>
						<v-col cols="3" class="border-right border-bottom">
						<p>Category</p> 
						</v-col>
						<v-col cols="3" class="border-right border-bottom">
							<span>
								{{ item.category }}
							</span>
						</v-col>
						<v-col cols="3" class="border-right border-bottom">
						<p>Monthly_cost</p> 
						</v-col>
						<v-col cols="3" class="border-bottom">
							<span>
								{{item.monthly_cost_savings}}
							</span>
						</v-col>

						<v-col cols="3" class="border-right border-bottom">
						<p>Impact</p> 
						</v-col>
						<v-col cols="3" class="border-right border-bottom">
							<span>
								{{ item.impact }}
							</span>
						</v-col>
						<v-col cols="3" class="border-right border-bottom">
							<p>Savings_currency</p> 
						</v-col>
						<v-col cols="3" class="border-bottom">
							<span>
								{{item.savings_currency}}
							</span>
						</v-col>

						<v-col cols="3" class="border-right border-bottom">
							<p>Problem</p> 
						</v-col>
						<v-col cols="3" class="border-right border-bottom">
							<span>
								{{ item.problem }}
							</span>
						</v-col>

						<v-col cols="3" class="border-right border-bottom resource">
							<div class="resource_group">
								<p>Resource_group</p> 
							</div>
							<div class="pl-3">
								<p>Resource</p> 
							</div>
							
						</v-col>
						<v-col cols="3" class="border-bottom resource">
							<div class="resource_group pb-2">
								<span>
									{{item.resource_group}}
								</span>
							</div>
							<div class="pl-3">
								<span>
									{{item.resource}}
								</span>
							</div>
						</v-col>

						<v-col cols="3" class="border-right border-bottom">
						<p>Solution</p> 
						</v-col>
						<v-col cols="3" class="border-right border-bottom">
							<span>
								{{ item.solution }}
							</span>
						</v-col>
						<v-col cols="3" class="border-right border-bottom">
						<p>Source</p> 
						</v-col>
						<v-col cols="3" class="border-bottom">
							<span>
								{{item.source}}
							</span>
						</v-col>

						<v-col cols="3" class="border-right border-bottom">
							<p>Resource_ID</p> 
						</v-col>
						<v-col cols="9" class="border-bottom">
							<span>{{ item.resource_id }}</span>
						</v-col>

						<v-col cols="3" class="border-right">
							<p>Recommendation</p> 
						</v-col>
						<v-col cols="9">
							<span>{{ item.recommendation }}</span>
						</v-col>

					</v-row>
                </v-col>
            </v-container>
           
              <v-col cols="4" class="pl-12">
                  <ButtonComponent :buttonName="'Move To ' + buttonName" @click="moveToActiveIgnore(buttonName)" />
              </v-col>
          </v-card>
        </v-dialog>
      </v-row>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { defineProps, defineEmits } from 'vue'
  import ButtonComponent from '../Buttons/Button.vue'

  
  const { resourcesName, dialog, item, buttonName } = defineProps(['resourcesName', 'dialog', 'item', 'buttonName']);
  const emit = defineEmits()
  
  const closeDialog = () => {
    emit('closeDialog', false)
  }
  
  const moveToActiveIgnore = (btn: String) => {
    emit('moveToActiveIgnore', btn)
  }
  </script>
  
  <style scoped>

		.main-content  {
			height: 400px;
    	overflow-y: scroll;
		}

		.scroll::-webkit-scrollbar-track {
			-webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
			border-radius: 5px;
		}

		.scroll::-webkit-scrollbar
		{
			width: 8px;
		}

		.scroll::-webkit-scrollbar-thumb
		{
			border-radius: 5px;
			-webkit-box-shadow: inset 0 0 6px rgba(0,0,0,.3);
			
		}




    .main-content p{
			color: var(--blue-blue-20, #013C6B);
			font-family: MB Corpo S Text WEB;
			font-size: 14px;
			font-style: normal;
			font-weight: 700;
			line-height: 20px; /* 142.857% */
    }

		.main-content span{
			color: var(--grey-grey-10, var(--grey-grey-90, #1A1A1A));
			font-family: MB Corpo S Text WEB;
			font-size: 15px;
			font-style: normal;
			font-weight: 400;
			line-height: 20px; /* 142.857% */
    }

		.border-right {
			border-right: 1px solid #DBDBDB;
		}
		
		.border-bottom {
			border-bottom: 1px solid #DBDBDB;
		}

		.resource {
			display: flex;
			flex-direction: column;
			justify-content: space-around;
			padding: 0;
		}

		.resource_group {
			border-bottom: 1px solid #DBDBDB;
			padding-left: 12px;
			padding-bottom: 11px;
		}
  
  </style>