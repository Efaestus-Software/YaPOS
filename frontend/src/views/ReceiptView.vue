<template>
    <div class="receipt-container justify-center flex flex-col py-4 px-2 spline text-xs cursor-pointer" @click="printReceipt" title="Click To Print">
        <!-- LOGO AND COMPANY DETAILS -->
        <div class="logo flex flex-col items-center justify-center">
            <!-- <span class="font-bold text-2xl">Logo</span> -->
            <!-- COMPANY NAME -->
            <span class="font-bold">{{business.name}}</span>
            <!-- CONTACT NO. -->
            <span class="mt-3">{{business.contact}}</span>
            <!-- EMAIL -->
            <span>{{business.email}}</span>
            <!-- WEBSITE -->
            <span>{{business.website}}</span>
            <!-- TIN -->
            <span>TIN: {{business.tin}}</span>
        </div>

        <!-- STARS -->

        <div class="flex flex-col items-center my-4">
            ************************
        </div>

        <!-- ITEMS -->
        <div class="flex flex-row justify-between mb-1" v-for="item in sales.salesitems">
            <div class="right-side flex items-start">
                <span class="mr-4">{{item.qty}}</span>
                <span>{{item.inventory.name}}</span>
            </div>

            <div class="left-side flex items-start ml-4">
                <span>{{formatPrice(item.amountTotal)}}</span>
            </div>
        </div>

        <!-- STARS -->

        <div class="flex flex-col items-center my-4">
            ************************
        </div>

        <!-- CALCULATIONS -->
        <div class="flex flex-col">
            <!-- SUBTOTAL -->
            <div class="flex flex-row justify-between">
                <span class="font-bold">Subtotal</span>
                <span>{{formatPrice(sales.subTotal)}}</span>
            </div>
            <!-- DISCOUNT -->
            <div class="flex flex-row justify-between">
                <span class="font-bold">Discount</span>
                <span>{{formatPrice(sales.discount)}}</span>
            </div>
            <!-- VAT EXEMPT -->
            <div class="flex flex-row justify-between">
                <span class="font-bold">VAT Exempt</span>
                <span>{{formatPrice(sales.vatExempt)}}</span>
            </div>
            <!-- VAT -->
            <div class="flex flex-row justify-between">
                <span class="font-bold">VAT</span>
                <span>{{formatPrice(sales.vat)}}</span>
            </div>
            <!-- TOTAL -->
            <div class="flex flex-row justify-between text-lg font-bold">
                <span class="font-bold">Total</span>
                <span>{{formatPrice(sales.total)}}</span>
            </div>
            <!-- PAYMENT -->
            <div class="flex flex-row justify-between">
                <span class="font-bold">Payment</span>
                <span>{{formatPrice(sales.payment)}}</span>
            </div>
            <!-- CHANGE -->
            <div class="flex flex-row justify-between text-lg font-bold">
                <span class="font-bold">Change</span>
                <span>{{formatPrice(sales.change)}}</span>
            </div>
        </div>

        <!-- STARS -->

        <div class="flex flex-col items-center my-4">
            ************************
        </div>

        <!-- ORDER NO. AND DATE -->
        <div class="flex flex-col">
            <div class="flex flex-row justify-center">
                <span>Invoice # {{sales.code}}</span>
            </div>
            <div class="flex flex-row justify-center">
                <span>{{formatDateTime(sales.date)}}</span>
            </div>
            <div class="flex flex-row justify-center">
                <span>Customer: 
                    <span v-if="sales.customer">{{sales.customer.name}}</span>
                    <span v-else-if="sales.temporaryCustomer">{{sales.temporaryCustomer}}</span>
                    <span v-else>Walk-in</span>
                </span>
            </div>
            <div class="flex flex-row justify-center" v-if="sales.seniorID">
                <span>Senior ID:
                    <span>{{sales.seniorID}}</span>
                </span>
            </div>
            <div class="flex flex-row justify-center items-center mt-2">
                <span class="text-center">{{business.address}}</span>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .receipt-container, body{
        width: 57mm !important;
    }
</style>

<script>
import {getAPI} from '@/axios-api.js'
import {mixins} from '@/mixins/mixins'
export default{
    mixins: [
        mixins
    ],
    data(){
        return{
            config:{
                headers: {
                    Authorization: `Bearer ${this.$store.state.accessToken}`
                }
            },

            business: {
                name: '',
                address: '',
                contact: '',
                email: '',
                website: '',
                tin: '',
            },

            sales: {
                change: 0,
                code: '',
                createdBy: {
                    first_name: '',
                    last_name: '',
                },
                customer: {
                    name: '',
                },
                temporaryCustomer: '',
                date: '',
                discount: 0,
                id: null,
                net: 0,
                payment: 0,
                salesitems: [],
                seniorID: '',
                subTotal: 0,
                total: 0,
                vat: 0,
                vatExempt: 0,
            }
        }
    },
    
    methods: {
        getBusiness(){
            return getAPI.get('/business-profile', this.config)
            .then(res => {
                this.business = res.data
            })
        },
        printReceipt(){
            window.print();
        },
        getSales(){
            return getAPI.get(`/sales/${this.$route.params.id}/`, this.config)
            .then(res => {
                this.sales = res.data
                console.log(this.sales)
            })
        },

        // onload(){
        //     return new Promise((resolve, reject) => {
        //         this.getBusiness()
        //         this.getSales()
        //         resolve()
        //     }).then(() => {
        //         window.print()
        //     })
        // }
    },
    async mounted(){
        await this.getBusiness()
        await this.getSales()
        window.print()
    }
}
</script>