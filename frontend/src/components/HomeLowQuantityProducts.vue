<template>
    <div class="w-full min-w-[28rem] h-[18rem] rounded-2xl shadow-lg bg-white lq-container flex flex-col">
        <!-- HEADER -->
        <div id="header" class="flex flex-row justify-between lq-text font-bold py-4 px-8">
            <span>Items</span>
            <span>Remaining</span>
        </div>

        <!-- ITEMS -->
        <div class="flex flex-col overflow-auto h-full pb-3">
            <div v-if="items.length" v-for="(item, index) in items" id="listItems" class="flex flex-row justify-between px-2 py-1 rounded-md mx-3" :class="index % 2 === 0 ? 'lq-list' : ''">
                <div class="flex flex-col font-bold">
                    <span>{{item.name}}</span>
                    <span class="lq-text">{{item.code}}</span>
                </div>
                <div class="flex flex-col font-bold items-end">
                    <span>{{item.qty}}</span>
                    <span class="lq-text">Pcs</span>
                </div>
            </div>

            <div v-else>
                <HLQPLoader v-if="loading" />
                <div v-else class="flex flex-row justify-center px-2 py-1 rounded-md mx-3 lq-list">
                    <div class="font-bold">
                        <span>No Items</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.lq-container{
    background-color: #FFC5C5;
}

.lq-text{
    color: #FF4848
}

.lq-list{
    background-color: #FF9494
}

::-webkit-scrollbar-thumb {
  background-color: #FF9494 !important;
  border-radius: 10px;
}

</style>

<script>
import { getAPI } from '@/axios-api'
import { mixins } from '@/mixins/mixins.js'
import HLQPLoader from './HLQPLoader.vue'
export default {
    components: {
        HLQPLoader
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

            loading: true,

            items: []
        }
    },

    async mounted(){
        this.loading = true
        await getAPI.get('/low-quantity-products/', this.config)
        .then(res=>{
            this.items = res.data
        })
        this.loading = false
    }
}
</script>