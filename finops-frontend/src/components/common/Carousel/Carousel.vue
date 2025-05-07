<template>
	<div>
		<HorizontalCard width="900" height="450" >
			<v-carousel v-model="model" hide-delimiters :show-arrows="false" class="carousel">
				<v-carousel-item v-for="(item, i) in carouseltem" :key="i" :value="i">
					<v-container class="pa-10">
						<v-row>
							<v-col cols="5">
								<p class="title d-flex align-center justify-start mb-5"> 
									{{ item.title }}
								</p>
								<p>
									{{ item.content }}
								</p>
							</v-col>
							<v-col cols="7" class="bg-technicaluser">
								<v-row>
									<v-col cols="10" class="d-flex align-center justify-start">
										<v-progress-linear
											:model-value="item.progress"
											color="light-blue"
										></v-progress-linear>
									</v-col>
									<v-col cols="2">
										{{ item.progress }}%
									</v-col>
								</v-row>
								<img :src="item.image" alt="Frame96" class="w-100 mt-10">
							</v-col>
						</v-row>
					</v-container>
				</v-carousel-item>
			</v-carousel>

			<div class="d-flex justify-center align-center py-4">
				<v-btn
					variant="text"
					icon="mdi-chevron-left"
					@click="model = Math.max(model - 1, 0)"
				></v-btn>
				<v-btn
					variant="text"
					icon="mdi-chevron-right"
					@click="model = Math.min(model + 1, 3)"
				></v-btn>
			</div>
		</HorizontalCard>
	</div>
</template>
  
 <script setup lang="ts">
	import { ref } from 'vue';
	import HorizontalCard from '../Cards/HorizontalCard.vue';
	import type { carouselItem } from '../../../utils/customInterface'

	const props = defineProps({
		carouseltem: Array<carouselItem>,
	})

	const model = ref(0)
  </script>

<style scoped>
	.carousel{
		height: auto !important;
	}

	.title {
		color: var(--blue-blue-20, #013C6B);
		font-family: MB Corpo S Text WEB;
		font-size: 20px;
		font-style: normal;
		font-weight: 700;
		line-height: 28px; /* 140% */
	}
</style>