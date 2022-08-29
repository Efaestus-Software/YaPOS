<template>
    <div class="w-full min-w-[28rem] h-[30rem] rounded-2xl shadow-lg bg-white lq-container flex flex-col">
        <!-- HEADER -->
        <div id="header" class="flex flex-row justify-between lq-text font-bold py-4 px-8">
            <span>Items</span>
            <span>Total Sales</span>
        </div>

        <!-- ITEMS -->
        <div class="flex flex-col overflow-auto h-full pb-3">
            <div v-if="items.length" v-for="(item, index) in items" id="listItems" class="flex flex-row justify-between px-2 py-1 rounded-md mx-3" :class="index % 2 === 0 ? 'bg-gray-100' : ''">
                <div class="flex flex-col font-bold">
                    <span>{{item.name}}</span>
                    <span class="text-gray-400">{{item.code}}</span>
                </div>
                <div class="flex flex-col font-bold items-end">
                    <span>{{item.sold}}</span>
                    <span class="text-gray-400">Sold</span>
                </div>
            </div>

            <div v-else>
                <HTPLoader v-if="loading"/>
                <div v-else class="flex flex-row justify-center px-2 py-1 rounded-md mx-3 bg-gray-100">
                    <div class="font-bold">
                        <span>No Items</span>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
</template>

<script>
import { getAPI } from '@/axios-api'
import { mixins } from '@/mixins/mixins.js'
import HTPLoader from './HTPLoader.vue'
export default {
    components: {
        HTPLoader
    },
    mixins: [
        mixins,
    ],
    methods: {
    },
    data() {
        return {
            config:{
                headers: {
                    Authorization: `Bearer ${this.$store.state.accessToken}`
                }
            },

            items: [],

            loading: false

        }
    },

    async mounted(){
        this.loading = true
        await getAPI.get('/top-products/', this.config)
        .then(res=>{
            this.items = res.data
        })

        this.loading = false
    }
}
</script>