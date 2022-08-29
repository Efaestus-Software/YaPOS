<template>

    <Nav />
    <SubNav>
        <template v-slot:body>
            <router-link to="/receive" id="sub-receive">Create</router-link>
            <router-link to="/rr-list" id="sub-rr-list">List</router-link>
        </template>
    </SubNav>

    <Transition name="fade" appear>
        <div class="xl:container xl:px-0 sm:px-4 mx-auto flex flex-col">
            <!-- TITLE -->
            <div class="mb-8">
                <span class="font-black text-3xl">RECEIVING REPORT</span>
            </div>

            <RRVueTable @toggle="toggle" :data="list" :header="['Code', 'Date', 'Supplier', 'Created By']" :dataIncluded="[['code'], ['date'], ['suppliers'], ['createdBy'],]" :enableSearch="true" :enableDate="true" :enableLink='true'/>
        </div>
    </Transition>
    
    <!-- MODAL 1 -->
    <Modal ref="rrDetailsModal" @close="toggleModal('rrDetailsModal')">
        <template v-slot:header>
            <div class="relative flex items-center p-6 bg-white rounded-t-xl min-w-[48rem]">
                <div class="flex w-fit flex-col rounded-lg bg-gray-100 p-3">
                    <span class="font-extrabold text-2xl">{{rrModal.code}}</span>
                    <span class="font-extrabold text-sm text-gray-400">{{toUpperCase(formatDate(rrModal.date))}}</span>
                </div>
                <i @click="toggleModal('rrDetailsModal')" class="absolute fa-solid fa-circle-xmark top-0 right-1 transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
            </div>
        </template>
        <template v-slot:body>
            <div class="bg-white flex flex-col gap-6">
                <div class="grid grid-cols-2 gap-y-8 px-6 py-5 bg-gray-100">
                    <div>
                        <label class="font-bold text-gray-400">Supplier</label><br>
                        <span class="font-extrabold text-xl" v-if="rrModal.suppliers">{{rrModal.suppliers.name}}</span>
                    </div>
                    <div>
                        <label class="font-bold text-gray-400">Created By</label><br>
                        <span class="font-extrabold text-xl" v-if="rrModal.createdBy">{{rrModal.createdBy.first_name}} {{rrModal.createdBy.last_name}}</span>
                    </div>
                    <div>
                        <label for="" class="font-bold text-gray-400">Total Amount</label><br>
                        <span class="font-extrabold text-xl">₱{{formatPrice(rrModal.amountTotal)}}</span>
                    </div>
                </div>
            </div>

            <div class="bg-white flex flex-col rounded-b-xl">
                <div class="px-6 pt-5">
                    <span class="font-extrabold text-2xl">Items</span>
                </div>

                <div class="flex flex-col gap-4 pt-4 pb-6 px-6">
                    <div v-for="item in rrModal.rritems" class="rounded-lg flex justify-between flex-row items-center my-shadow p-3">
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
import RRVueTable from '@/components/RRVueTable.vue'
import { getAPI } from '@/axios-api'
import Modal from '@/components/Modal.vue'

export default{
    mixins: [
        mixins
    ],
    components: {
        Nav,
        SubNav,
        RRVueTable,
        Modal
    },
    data(){
        return{
            config:{
                headers: {
                    Authorization: `Bearer ${this.$store.state.accessToken}`
                }
            },

            list: [{
                id: '',
                code: '',
                date: '',
                supplier: '',
                createdBy: '',
            }],

            rrModal: {
                id: '',
                code: '',
                date: '',
                suppliers: {
                    name: ''
                },
                createdBy: {
                    first_name: '',
                    last_name: ''
                },
                rritems: [{
                    id: null,
                    remaining: null,
                    unitCost: 0,
                    amountTotal: 0,
                    qty: 0,
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
    methods: {
        toggle(id){
            this.toggleModal('rrDetailsModal')
            this.rrModal = this.list.find(item=>item.id == id)
        },

        toggleModal(id){
            this.$refs[id].showModal = !this.$refs[id].showModal
        },

        getRR(){
            getAPI.get('/receiving-report/', this.config)
            .then(res => {
                this.list = res.data
            })
        },

        toUpperCase(str){
            return str.toUpperCase()
        },
    },

    mounted(){
        this.getRR()
    }
}

</script>