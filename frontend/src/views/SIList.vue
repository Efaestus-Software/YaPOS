<template>

    <Nav />
    <SubNav>
        <template v-slot:body>
            <router-link to="/si-list" id="sub-si-list">Sales Invoice</router-link>
        </template>
    </SubNav>

    <Transition name="fade" appear>
        <div class="xl:container xl:px-0 sm:px-4 mx-auto flex flex-col">
            <!-- TITLE -->
            <div class="mb-8" id="hello">
                <span class="font-black text-3xl">SALES INVOICE</span>
            </div>

            <SIVueTable class="mb-8" @toggle="toggle" :data="order" :header="['Code', 'Date', 'Customer', 'Created By', 'Total']" :dataIncluded="[['code'], ['date'], ['customers'], ['createdBy'], ['amountTotal']]" :enableSearch="true" :enableLink="true" :enableDate="true" :loading="loading" />
        </div>
    </Transition>

    <!-- MODAL 1 -->
    <Modal ref="salesDetails" @close="toggleModal('salesDetails')">
        <template v-slot:header>
            <div class="relative flex items-center p-6 bg-white rounded-t-xl min-w-[48rem]">
                <div class="flex w-fit flex-col rounded-lg bg-gray-100 p-3" :class="{'bg-red-100':salesDetails.void}">
                    <span class="font-extrabold text-2xl" :class="{'text-red-500':salesDetails.void}">Invoice # {{salesDetails.code}}</span>
                    <span class="font-extrabold text-sm" :class="[salesDetails.void ? 'text-red-400' : 'text-gray-400']">{{formatDateTime(salesDetails.date)}} <span class="font-black" v-if="salesDetails.void">Voided</span> </span>
                </div>

                <div class="ml-4" v-if="!salesDetails.void">
                    <button class="btn-void" @click="voidSales(salesDetails.id)">Void</button> 
                </div>

                <div class="ml-4">
                    <span class="link font-medium" @click="createReceipt(salesDetails.id)">Create a Receipt</span>
                </div>
                <i @click="toggleModal('salesDetails')" class="absolute fa-solid fa-circle-xmark top-0 right-1 transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
            </div>
        </template>

        <template v-slot:body>
            <div class="bg-white flex flex-col gap-6">
                <div class="grid grid-cols-2 gap-y-8 px-6 py-5 bg-gray-100">
                    <div>
                        <label class="font-bold text-gray-400">Customer</label><br>
                        <span class="font-extrabold text-xl" v-if="salesDetails.customer">{{salesDetails.customer.name}}</span>
                        <span class="font-extrabold text-xl" v-else-if="salesDetails.temporaryCustomer">{{salesDetails.temporaryCustomer}}</span>
                        <span class="font-extrabold text-xl text-red-400" v-else>Walk-in Customer</span>
                    </div>
                    <div>
                        <label class="font-bold text-gray-400">Created By</label><br>
                        <span class="font-extrabold text-xl" v-if="salesDetails.createdBy">{{salesDetails.createdBy.first_name}} {{salesDetails.createdBy.last_name}}</span>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-y-8 px-6 py-5 bg-gray-100">
                    <div>
                        <label for="" class="font-bold text-gray-400">Sub-Total</label><br>
                        <span class="font-extrabold text-xl">₱{{formatPrice(salesDetails.subTotal)}}</span>
                    </div>

                    <div>
                        <label for="" class="font-bold text-gray-400">VAT</label><br>
                        <span class="font-extrabold text-xl">₱{{formatPrice(salesDetails.vat)}}</span>
                    </div>

                    <div>
                        <label for="" class="font-bold text-gray-400">VAT Exempt</label><br>
                        <span class="font-extrabold text-xl">₱{{formatPrice(salesDetails.vatExempt)}}</span>
                    </div>

                    <div>
                        <label for="" class="font-bold text-gray-400">Net</label><br>
                        <span class="font-extrabold text-xl">₱{{formatPrice(salesDetails.net)}}</span>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-y-8 px-6 py-5 bg-gray-100">
                    <div>
                        <label for="" class="font-bold text-gray-400">Discount</label><br>
                        <span class="font-extrabold text-xl">₱{{formatPrice(salesDetails.discount)}}</span>
                    </div>

                    <div>
                        <label for="" class="font-bold text-gray-400">Senior Citizen</label><br>
                        <span class="font-extrabold text-xl">{{salesDetails.seniorID ? 'Yes' : 'No'}}</span>
                        <span class="font-bold text-base ml-2 text-gray-500" v-if="salesDetails.seniorID">{{salesDetails.seniorID}}</span>
                    </div>
                    
                    
                    <div>
                        <label for="" class="font-bold text-gray-400">Total</label><br>
                        <span class="font-extrabold text-xl">₱{{formatPrice(salesDetails.total)}}</span>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-y-8 px-6 py-5 bg-gray-100">
                    <div>
                        <label for="" class="font-bold text-gray-400">Payment</label><br>
                        <span class="font-extrabold text-xl">₱{{formatPrice(salesDetails.payment)}}</span>
                    </div>

                    <div>
                        <label for="" class="font-bold text-gray-400">Change</label><br>
                        <span class="font-extrabold text-xl">₱{{formatPrice(salesDetails.change)}}</span>
                    </div>
                </div>
            </div>

            <div class="bg-white flex flex-col rounded-b-xl">
                <div class="px-6 pt-5">
                    <span class="font-extrabold text-2xl">Items</span>
                </div>

                <div class="flex flex-col gap-4 pt-4 pb-6 px-6">
                    <div v-for="item in salesDetails.salesitems" class="rounded-lg flex justify-between flex-row items-center my-shadow p-3">
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
                            <span class="font-bold">₱{{formatPrice(item.inventory.sellingPrice)}}</span>
                            <span class="font-bold text-sm text-gray-400">Selling Price</span>
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
import SIVueTable from '@/components/SIVueTable.vue'
import {getAPI} from '@/axios-api.js'
import Modal from '@/components/Modal.vue'
import { Printd } from 'printd'

export default {
    data() {
        return {
            config: {
                headers: {
                    Authorization: `Bearer ${this.$store.state.accessToken}`
                }
            },
            order: [],

            loading: false,

            salesDetails: {
                customer: {
                    name: '',
                },
                date: '',
                temporaryCustomer: '',
                code: '',
                seniorID: '',
                items: [],
                discount: 0,
                discountPercent: 0,
                vatExempt: 0,
                vat: 0,
                net: 0,
                total: 0,
                subTotal: '',
                payment: '',
                change: 0,
                createdBy: {
                    first_name: '',
                    last_name: ''
                },
            }
        }
    },
    
    methods: {
        async getSales(){
            return getAPI('/sales/', this.config)
            .then(res=>{
                this.order = res.data
            })
        },
        
        async onload(){
            return this.getSales()
        },

        toggle(id){
            this.toggleModal('salesDetails')
            this.salesDetails = this.order.find(order => order.id == id)
        },

        createReceipt(id){
            const route = this.$router.resolve('/receipt/' + id);
            window.open(route.href, '_blank');
        },

        resetSalesDetails(){
            this.salesDetails = {
                customer: {
                    name: '',
                },
                date: '',
                temporaryCustomer: '',
                code: '',
                seniorID: '',
                items: [],
                discount: 0,
                discountPercent: 0,
                vatExempt: 0,
                vat: 0,
                net: 0,
                total: 0,
                subTotal: '',
                payment: '',
                change: 0,
                createdBy: {
                    first_name: '',
                    last_name: ''
                },
            }
        },

        voidSales(id){
            // getAPI.post(`/void-sales/${id}`,{} ,this.config)
            this.$swal({
                buttonsStyling: false,
                customClass: {
                    confirmButton: 'btn-danger',
                    cancelButton: 'btn mr-2',
                },
                title: "Are you sure?",
                html: 'Are you sure you want to void this invoice? <br><br> <strong>This action cannot be undone.</strong>',
                icon: 'warning',
                showCancelButton: true,
                reverseButtons: true, 
                confirmButtonText: 'Void',
                cancelButtonText: 'Cancel',
            }).then(result=>{
                if(result.isConfirmed){
                    console.log('CONFIRMED')
                    getAPI.post(`/void-sales/${id}/`,{} ,this.config)
                    .then(res=>{
                        if(res.data == 0){
                            this.getSales()
                            this.toggleModal('salesDetails')
                            this.swalSuccess('Void Successful')
                            this.resetSalesDetails()
                        }
                        else if(res.data == 1){
                            this.swalWarning('Invoice is already voided.')
                        }
                    })
                    .catch(err=>{
                        this.swalError('Void Failed \n' + err.message)
                    })
                }
            })
        }
    },

    async mounted(){
        this.loading = true
        await this.onload()
        this.loading = false
    },

    mixins: [
        mixins
    ],
    components: {
        Nav,
        SubNav,
        VueTable,
        SIVueTable,
        Modal
    },
}

</script>