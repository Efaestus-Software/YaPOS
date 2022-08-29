<template>

    <Nav />
    <SubNav>
        <template v-slot:body>
            <router-link to="/adjustments" id="sub-adjustments">Create</router-link>
            <router-link to="/ad-list" id="sub-ad-list">List</router-link>
        </template>
    </SubNav>

    <Transition name="fade" appear>
        <div class="xl:container xl:px-0 sm:px-4 mx-auto flex flex-col">
            <!-- TITLE -->
            <div class="mb-8">
                <span class="font-black text-3xl">ADJUSTMENTS</span>
            </div>

            <ADVueTable @toggle="toggle" :data="list" :header="['Code', 'Date', 'Created By']" :dataIncluded="[['code'], ['date'], ['createdBy']]" :enableSearch="true" :enableDate="true" :enableLink="true" />
        </div>
    </Transition>


    <!-- MODAL 1 -->
    <Modal ref="adDetailsModal" @close="toggleModal('adDetailsModal')">
        <template v-slot:header>
            <div class="relative flex items-center p-6 bg-white rounded-t-xl min-w-[48rem]">
                <div class="flex w-fit flex-col rounded-lg bg-gray-100 p-3">
                    <span class="font-extrabold text-2xl">{{adModal.code}}</span>
                    <span class="font-extrabold text-sm text-gray-400">{{toUpperCase(formatDate(adModal.date))}}</span>
                </div>
                <i @click="toggleModal('adDetailsModal')" class="absolute fa-solid fa-circle-xmark top-0 right-1 transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
            </div>
        </template>
        <template v-slot:body>
            <div class="bg-white flex flex-col gap-6">
                <div class="grid grid-cols-2 gap-y-8 px-6 py-5 bg-gray-100">
                    <div>
                        <label class="font-bold text-gray-400">Adjustment Type</label><br>
                        <span class="font-extrabold text-xl" v-if="adModal.type">{{adModal.type}}</span>
                    </div>
                    <div>
                        <label class="font-bold text-gray-400">Created By</label><br>
                        <span class="font-extrabold text-xl" v-if="adModal.createdBy">{{adModal.createdBy.first_name}} {{adModal.createdBy.last_name}}</span>
                    </div>
                    <div>
                        <label for="" class="font-bold text-gray-400">Total Lost</label><br>
                        <span class="font-extrabold text-xl">₱{{formatPrice(adModal.amountTotal)}}</span>
                    </div>
                </div>
            </div>

            <div class="bg-white flex flex-col rounded-b-xl">
                <div class="px-6 pt-5">
                    <span class="font-extrabold text-2xl">Items</span>
                </div>

                <div class="flex flex-col gap-4 pt-4 pb-6 px-6">
                    <div v-for="item in adModal.aditems" class="rounded-lg flex justify-between flex-row items-center my-shadow p-3">
                        <!-- NAME AND CODE -->
                        <div class="flex flex-1 flex-col">
                            <span class="font-bold" v-if="item.inventory">{{item.inventory.name}}</span>
                            <span class="font-bold text-sm text-gray-400" v-if="item.inventory">{{item.inventory.code}}</span>
                        </div>
                        
                        <!-- QTY -->
                        <div class="flex flex-1 flex-col">
                            <span class="font-bold">{{item.qty}} pcs</span>
                            <span class="font-bold text-sm text-gray-400">Qty</span>
                        </div>

                        <!-- UNIT COST -->
                        <div class="flex flex-1 flex-col">
                            <span class="font-bold">₱{{formatPrice(item.unitCost)}}</span>
                            <span class="font-bold text-sm text-gray-400">Unit Cost</span>
                        </div>

                        <!-- TOTAL -->
                        <div class="flex flex-1 flex-col">
                            <span class="font-bold">₱{{formatPrice(item.amountTotal)}}</span>
                            <span class="font-bold text-sm text-gray-400">Total</span>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </Modal>
</template>

<script>

import Nav from '@/components/Nav.vue'
import SubNav from '@/components/SubNav.vue'
import { mixins } from '@/mixins/mixins.js'
import VueTable from '@/components/VueTable.vue'
import ADVueTable from '@/components/ADVueTable.vue'
import { getAPI } from '@/axios-api'
import Modal from '@/components/Modal.vue'

export default{
    data(){
        return{
            config:{
                headers: {
                    Authorization: `Bearer ${this.$store.state.accessToken}`
                }
            },
            list: [],

            adModal: {
                id: '',
                code: '',
                date: '',
                createdBy: {
                    first_name: '',
                    last_name: ''
                },
                aditems: [{
                    id: null,
                    remaining: null,
                    unitCost: 0,
                    amountTotal: 0,
                    qty: 0,
                    type: '',
                    inventory: {
                        id: null,
                        code: null,
                        name: null,
                        qty: null,
                        sellingPrice: 0,
                        unitCost: 0,
                    }
                }]
            },
        }
    },
    mixins: [
        mixins
    ],
    components: {
        Nav,
        SubNav,
        VueTable,
        ADVueTable,
        Modal
    },

    methods: {
        toggle(id){
            this.toggleModal('adDetailsModal')
            this.adModal = this.list.find(item=>item.id == id)
        },

        toggleModal(id){
            this.$refs[id].showModal = !this.$refs[id].showModal
        },

        getAD(){
            getAPI.get('/adjustment/', this.config)
            .then(res => {
                this.list = res.data
            })
            .catch(err =>{
                if(err.message.includes('403')){
                    this.swalWarning('You are not authorized to access this page.')
                }
            })
        },

        toUpperCase(str){
            return str.toUpperCase()
        },
    },

    mounted(){
        this.getAD()
    }
}

</script>