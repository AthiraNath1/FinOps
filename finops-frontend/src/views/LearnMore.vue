<template>
    <div>
      <!-- Header Component -->
      <HeaderComponent />
  
      <!-- Login Page Content Component-->
      <v-col cols="12" class="top-panel mt-16">
        <BreadCrumbs :items="breadcrumbItem" />
  
        <v-btn variant="text" class="back-btn" @click="onclickBackBtn()">
          <v-icon start icon="mdi-chevron-left" color="#036DC1" size="x-large" ></v-icon>
          Back
        </v-btn>
  
        <div class="w-100 d-flex align-center justify-center top-panel-conent">
          <span>{{ topPanelValue }}</span>
        </div>
      </v-col>
		
      <v-col cols="12" class="d-flex align-center justify-center mt-5" v-if="selectedUser == true">
				<v-col
					cols="2"
					class="mt-5"
					@click="selectedCard(2, 'Technical')"
					:class="{ active: activeCard === 1 }"
				>
					<v-card
						variant="outlined"
						class="d-flex align-center justify-center flex-column card"
						height="200px"
					>
						<img width="100" height="100" src="/src/assets/images/Technical.jpeg" />
						<v-card-title class="heading">Technical User</v-card-title>

					</v-card>
				</v-col>

				<v-col 
					cols="2"
					class="mt-5"
					@click="selectedCard(1, 'Business')"
					:class="{ active: activeCard === 2 }"
				>
					<v-card
						variant="outlined"
						class="d-flex align-center justify-center flex-column card"
						height="200px"
					>
						<img width="100" height="100" src="/src/assets/images/Business.jpeg" />
						<v-card-title class="heading">Business User</v-card-title>
					</v-card>
				</v-col>
      </v-col>

			<HorizontalCard width="900" height="450" class="mt-16" v-if="technicalUser == true">
			 <v-container class="pa-10">
				<v-row>
					<v-col cols="5">
						<p class="title d-flex align-center justify-start mb-5">
							<img src="/src/assets/images/target.jpeg" alt="">
							Advantages of FinX
						</p>
						<v-col cols="12">
							<ul>
								<li class="content">
									Single application to analyze and optimize cloud spend
								</li>
								<li class="content">
									Review and action on cloud advisory recommendations
								</li>
								<li class="content">
									Optimize and Clean up of Orphan and low-utilized cloud resources
								</li>
							</ul>
						</v-col>
						<v-btn variant="outlined" class="button mt-5" @click="selectedCard(1, 'Business')">
							View Business User Benefits
						</v-btn>
						
					</v-col>
					<v-col cols="7" class="bg-technicaluser">
						<img src="/src/assets/images/Frame96.jpeg" alt="Frame96" class="w-100">
						<v-btn class="story" variant="text" @click="onStory">View Jennifer’s  Story</v-btn>
					</v-col>
			 </v-row>
			 </v-container>
			</HorizontalCard>

			<HorizontalCard width="900" height="450" class="mt-16" v-if="businessUser == true">
			 <v-container class="pa-10">
				<v-row>
					<v-col cols="5">
						<p class="title d-flex align-center justify-start mb-5">
							<img src="/src/assets/images/target.jpeg" alt="">
							Advantages of FinX
						</p>
						<v-col cols="12">
							<ul>
								<li class="content">
									Transparency to Cloud investments
								</li>
								<li class="content">
									Executive dashboard for cost analysis and management with instant reports
								</li>
								<li class="content">
									Plan and Budget Cloud investments
								</li>
								<li class="content">
									Monitoring and alerting Cloud spend
								</li>
							</ul>
						</v-col>
						<v-btn variant="outlined" class="button mt-5" @click="selectedCard(2, 'Technical')">
							View Technical User
						</v-btn>
						
					</v-col>
					<v-col cols="7" class="bg-businessuser">
						<img src="/src/assets/images/happymanager.jpeg" alt="happymanager" class="mt-5">
						<v-btn class="story" variant="text" @click="onStory">View Mathew’s  Story</v-btn>
					</v-col>
			 </v-row>
			 </v-container>
			</HorizontalCard>

      <Carousel :carouseltem="carouseltem" v-if="viewStory"/>
      
      <!-- Footer Component -->
      <FooterComponent />
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
	import { useRouter } from 'vue-router'
  import HeaderComponent from '../components/common/Header.vue'
  import FooterComponent from '../components/common/Footer.vue'
  import BreadCrumbs from '../components/common/BreadCrumbs.vue'
	import HorizontalCard from '../components/common/Cards/HorizontalCard.vue'
	import Carousel from '../components/common/Carousel/Carousel.vue'

	import Frame96 from '../assets/images/Frame96.jpeg'
	import TechnicalUser2 from '../assets/images/TechnicalUser-2.jpeg'
	import TechnicalUser3 from '../assets/images/TechnicalUser-3.jpeg'
	import TechnicalUser4 from '../assets/images/TechnicalUser-4.jpeg'
	import BusinessUser1 from '../assets/images/BusinessUser-1.jpeg'
	import BusinessUser2 from '../assets/images/BusinessUser-2.jpeg'
	import BusinessUser3 from '../assets/images/BusinessUser-3.jpeg'
	import Frame95 from '../assets/images/Frame95.jpeg'

	const router = useRouter()

  let topPanelValue = ref<string>('How FinX helps it’s users');
	let selectedUser = ref<boolean>(true);
	let technicalUser = ref<boolean>(false);
	let businessUser = ref<boolean>(false);
	let viewStory = ref<boolean>(false);
	let currentValueBack = ref<string>('');
	let seletedCardName = ref<string>('');

  let breadcrumbItem = ref([
    {
      title: 'Login/SignUp',
      disabled: false
    },
    {
      title: 'Choose Platform',
      disabled: true
    }
  ]);
	
	let carouseltem = ref([
	{
			title: "",
			content: "",
			progress: "",
			image: "",
		}
	]);
	
	let technicalUsercarouseltem = ref([
		{
			title: "Meet Jennifer - Part 1 /4",
			content: "Jennifer is working as a senior cloud architect at Mercedes Benz. One day while she was  checking upon a project," +
			"she realized there is a increase in the cost. She noticed a similar pattern in various other projects.",
			progress: "25",
			image: Frame96,
		},
		{
			title: "Meet Jennifer - Part 2 /4",
			content: "She was concerned about this surge but she did not have enough time to invest each issues one by one." +
			" She figured that there were orphan resources that needs to be cleaned. But with here meetings, reports - figuring these resources is so time consuming",
			progress: "50",
			image: TechnicalUser2,
		},
		{
			title: "Meet Jennifer - Part 3 /4",
			content: "A friend of hers at Benz told her about this new application that is made for optimizing cloud expense by various measures called FinX.",
			progress: "75",
			image: TechnicalUser3,
		},
		{
			title: "Meet Jennifer - Part 4 /4",
			content: "FinX takes care of efficiently removing the orphan resources, recommending options for cost optimization." + 
			" With the help of FinX, she was able to identify and delete the cloud resources responsible for unwanted costs.",
			progress: "100",
			image: TechnicalUser4,
		},
	]);

	let businessUsercarouseltem = ref([
		{
			title: "Meet Mathew - Part 1 /4",
			content: "Mathew is a IT Operations Manager and he was creating a budget forecast. As he had cut down of many resources." + 
			" He was sure about his cost optimization. But his forecast did not look as favorable as expected.",
			progress: "25",
			image: BusinessUser1,
		},
		{
			title: "Meet Mathew - Part 2 /4",
			content: "He decided to try FinX - the new FinOps Application developed by Mercedes Benz." +
			"With few clicks, the app showed him the orphan resources, underutilised resources. " +
			"All these were not easy to identify when done manually and used to take a lot of his time",
			progress: "50",
			image: BusinessUser2,
		},
		{
			title: "Meet Mathew - Part 3 /4",
			content: "User friendly data visualization and data summary. Easy dashboards, summary charts and cost optimization measures." +
			"Now Cost Analysis - is just  a few clicks!",
			progress: "75",
			image: BusinessUser3,
		},
		{
			title: "Meet Mathew - Part 4 /4",
			content: "Mathew is impressed by FinX. Finally he feels there is an application that could really help him manage expenses without making him crunch" +
			"data even for the simplest thing." + 
			"Mathew finds an effective tool that gives him data to communicate properly to all his colleagues with ease.",
			progress: "100",
			image: Frame95,
		},
	])
  
  const activeCard = ref(0);
  const selectedCard = (cardNumber: number, cardName: string) => {
		activeCard.value = activeCard.value === cardNumber ? 0 : cardNumber
		selectedUser.value = false;
		currentValueBack.value = "user";
		seletedCardName.value = cardName;
		// On select card
		if(seletedCardName.value === 'Technical') {
			technicalUser.value = true;
			businessUser.value = false;
			topPanelValue.value = 'Technical User'
			breadcrumbItem.value = [
				{
					title: 'Login/SignUp',
					disabled: false
				},
				{
					title: 'Select User',
					disabled: false
				},
				{
					title: 'Technical User',
					disabled: true
				}
			];
			carouseltem.value = technicalUsercarouseltem.value;
		}
		else {
			businessUser.value = true;
			technicalUser.value = false;
			topPanelValue.value = 'Business User'
			breadcrumbItem.value = [
				{
					title: 'Login/SignUp',
					disabled: false
				},
				{
					title: 'Select User',
					disabled: false
				},
				{
					title: 'Business User',
					disabled: true
				}
			];
			carouseltem.value = businessUsercarouseltem.value;
		}
  }

	const onStory = () => {
		currentValueBack.value = "story";
		viewStory.value = true;
		technicalUser.value = false;
		businessUser.value = false;
	}

	const onclickBackBtn = () => {
		console.log("currentValueBack.value", currentValueBack.value)
		if(currentValueBack.value == "user") {
			selectedUser.value = true;
			technicalUser.value = false;
			businessUser.value = false;
			topPanelValue.value = 'How FinX helps it’s users';
			currentValueBack.value = ""
		}else if(currentValueBack.value == "story" ) {
			if(seletedCardName.value === 'Technical'){
				technicalUser.value = true;
				businessUser.value = false;
				currentValueBack.value = "user";
				viewStory.value = false;
			}else  {
				businessUser.value = true;
				technicalUser.value = false;
				currentValueBack.value = "user";
				console.log("3333333333333--------e", currentValueBack.value)
				if(currentValueBack.value == "") {
					router.push('/')
				}
				viewStory.value = false;
			}
		}else if(currentValueBack.value == "") {
					router.push('/')
		}
	};
  
  
  </script>
  
  <style scoped>
  .top-panel {
    background: var(--blue-blue-95, #e6f5ff);
    width: 100%;
    height: 160px;
    flex-shrink: 0;
    position: relative;
  }
  
  .breadcrumbs {
    color: var(--wb-grey-20, #333);
    font-family: MB Corpo S Text WEB;
    font-size: 12px;
    font-style: normal;
    font-weight: 400;
    line-height: 16px;
    letter-spacing: 0.2px;
  }
  
  .top-panel-conent {
    color: #000;
    text-align: center;
    font-family: MB Corpo A Text Cond WEB;
    font-size: 40px;
    font-style: normal;
    font-weight: 400;
    line-height: 48px;
    position: absolute;
    top: 0;
    bottom: 0;
  }

  
  .card {
    border-radius: 4px;
		border: 1px solid var(--blue-blue-90, #CCE8FF);
		background: #FFF;
  }
  
  .sign-card {
    border-radius: 12px;
    border: 1px solid var(--blue-blue-90, #cce8ff);
    box-shadow: 2px 5px 6px 0px rgba(0, 0, 0, 0.1);
  }
  
	.heading{
		color: #000;
		font-family: MB Corpo S Title WEB;
		font-size: 20px;
		font-style: normal;
		font-weight: 400;
		line-height: 32px; 
	}

	.title {
		color: var(--blue-blue-20, #013C6B);
		font-family: MB Corpo S Text WEB;
		font-size: 20px;
		font-style: normal;
		font-weight: 700;
		line-height: 28px; /* 140% */
	}

	.button {
		border: 1px solid var(--blue-blue-50, #008DFC);
		color: var(--blue-blue-50, #008DFC);
		text-align: center;
		font-family: MB Corpo S Text WEB;
		font-size: 14px;
		font-style: normal;
		font-weight: 400;
		line-height: 20px;
		text-transform: capitalize;
		border-radius: 0px;
	}

	.bg-technicaluser{
		text-align: center;
	}

	.bg-businessuser{
		background: url('/src/assets/images/Frame95.jpeg');
		background-repeat: no-repeat;
    background-size: contain;
		text-align: end;
	}

	.story {
		color: var(--blue-blue-40, #036DC1);
		font-family: MB Corpo S Text WEB;
		font-size: 14px;
		font-style: normal;
		font-weight: 400;
		line-height: 20px;
		text-decoration-line: underline;
		text-align: center;
		text-transform: capitalize;
	}

	.back-btn {
		z-index: 9;
	}
  
  

  
  </style>