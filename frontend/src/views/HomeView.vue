<template>
    <Nav />
    <Transition name="fade" appear>
        <div class="container mx-auto flex flex-col items-center">
            <div>
                <!-- TITLE -->
                <div class="mb-8 mt-3 flex justify-between">
                    <span class="font-black text-3xl">HOME</span>
                    <!-- FANCY CLOCK -->
                    <FancyClock/>
                </div>

                <div class="flex sm:flex-col xl:flex-row gap-12 pb-12">
                    <div class="flex flex-col gap-8">
                        <span class="font-extrabold text-2xl">Performance</span>
                        <div class="flex flex-row gap-8">
                            <!-- SALES FOR THE MONTH COMPONENT -->
                            <HSFM/>
                            <!-- SALES FOR THE DAY COMPONENT -->
                            <HSFD/>
                        </div>

                        <span class="font-extrabold text-2xl">Statistics</span>
                        <!-- SALES GRAPH COMPONENT -->
                        <HSG/>
                    </div>
                    <div class="flex flex-col gap-8">
                        <span class="font-extrabold text-2xl">Low Stock Products</span>
                        <!-- LOW QUANTITY PRODUCTS COMPONENT -->
                        <HLQP/>
                        <span class="font-extrabold text-2xl">Top Products</span>
                        <!-- TOP PRODUCTS COMPONENT -->
                        <HTP/>
                    </div>
                </div>
            </div>
        </div>
    </Transition>

</template>

<script>
import Nav from '@/components/Nav.vue'
import { mixins } from '@/mixins/mixins.js'
import { getAPI } from '@/axios-api'
import Modal from '@/components/Modal.vue'
import HSFM from '@/components/HomeSalesForMonth.vue'
import HSG from '@/components/HomeSalesGraph.vue'
import HTP from '@/components/HomeTopProducts.vue'
import HSFD from '@/components/HomeSalesForDay.vue'
import HRS from '@/components/HomeRecentSales.vue'
import HLQP from '@/components/HomeLowQuantityProducts.vue'
import FancyClock from '@/components/FancyClock.vue'

export default{
    components: {
        Nav,
        Modal,
        HSFM,
        HSG,
        HTP,
        HSFD,
        HRS,
        HLQP,
        FancyClock
    },
    mixins: [
        mixins
    ],
    methods: {
        logout(){
            this.$router.push({name: 'logout'})
        },
    },

    mounted(){
        getAPI.get('/business-profile/')
        .then(res=>{
            console.log('has business profile')
        })
        .catch(err=>{
            this.$swal({
                buttonsStyling: false,
                customClass: {
                    confirmButton: 'btn-primary mr-2',
                    cancelButton: 'btn btn-danger',
                },
                title: 'Setup your Business Profile',
                html: 'Problems may occur if you do not setup your business profile. <br/> <br/> <b>Do you want to setup your business profile?</b>',
                showConfirmButton: true,
                showCancelButton: true,
                confirmButtonText: 'Setup',
                cancelButtonText: 'Dismiss',
            })
            .then(result=>{
                if(result.isConfirmed){
                    this.$router.push({name: 'business-settings'})
                }
            })
        })
    }
}
</script>