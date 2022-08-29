<template>
    <div class="greenBox w-[28rem] h-[18rem] rounded-2xl shadow-lg bg-white p-6 justify-between flex flex-col relative overflow-hidden">
        <span class="z-10 font-bold">Sales for the Month</span>
        <span class="z-10 font-black text-4xl montserrat" v-if="!loading">₱{{formatPrice(totalSales)}}</span>
        <div class="z-10" v-else>
            <div class="grid grid-cols-12">
                <div class="h-2 bg-green-300 animate-pulse rounded col-span-8"></div>
            </div>
        </div>
        <img src="@/assets/orangeBlob.svg" class="select-none absolute top-0 right-0" alt="">
        <img src="@/assets/greenBlobl.svg" class="select-none absolute bottom-0 right-0" alt="">
    </div>
</template>

<style scoped>
    span{
        color: #c5ffc4
    }

    .greenBox{
        background-color: #21D11E;
    }
</style>

<script>
import { getAPI } from '@/axios-api'
import { mixins } from '@/mixins/mixins.js'

export default {
    components: {
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

            totalSales: 0,

            loading: false,
        }
    },

    async mounted(){
        this.loading = true
        await getAPI.get('/sales-for-the-month/', this.config)
        .then(res=>{
            this.totalSales = res.data
        })
        this.loading = false
    }
}
</script>