<style scoped>
    .menu-item-header{
        background-color: rgba(255,255,255,0.75);
        backdrop-filter:blur(25px);
    }
</style>
<template>
    <div class="flex flex-col h-screen w-screen max-h-screen max-w-screen relative">
        <Nav />
        <Transition name="fade" appear>
            <div class="flex flex-1 px-5 pb-5 gap-5 max-w-screen" style="min-height:0">
                <!-- LEFT PANE -->
                <div id="left" class="flex flex-col shrink-0 bg-white max-h-full rounded-xl shadow-2xl w-1/3 divide-y">
                    <!-- SALES HEADER -->
                    <div class="flex flex-rol items-center px-5 py-5 justify-between ">
                        <!-- NUMBER AND VOID -->
                        <div class="flex items-center gap-3">
                            <span class="text-gray-400 text-xl font-semibold">Invoice # {{order.code}}</span>
                            <button class="btn-void" @click="resetData">Reset</button> 
                        </div>

                        <!-- ADD CUSTOMER -->
                        <div @click="toggleModal('addCustomer')" class="flex text-ellipsis truncate whitespace-nowrap items-center text-gray-400 font-semibold cursor-pointer h-full  px-2 rounded-md hover:bg-gray-100">
                            <span>
                                <i class="fa-solid fa-user mr-1"></i>
                                <span v-if="order.existingCustomer || order.temporaryCustomer">{{this.order.temporaryCustomer ? this.order.temporaryCustomer : getCustomerName(this.order.existingCustomer)}}</span>
                                <span v-else>Add Customer +</span>
                            </span>
                        </div>
                    </div>

                    <!-- SALES ITEMS -->
                    <div class="flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
                        <TransitionGroup name="list">
                            <div class="select-none flex flex-row transition justify-between items-center py-3 px-5 hover:bg-gray-100" v-for="(item, index) in order.items" @contextmenu.prevent="deductItem(index)" :key="item">
                                <!-- LEFT SIDE -->
                                <div class="flex flex-0 items-center relative w-full" @click="editItem(item)">
                                    <!-- COUNTER -->
                                    <div class="absolute rounded-full bg-sky-400 h-6 w-6 -top-2 left-6 flex items-center justify-center text-sm font-bold text-white">
                                        {{item.qty}}
                                    </div>
    
                                    <img v-if="item.inventory.image" :src="getBaseURL() + item.inventory.image" class="rounded-full h-full h-10 w-10 mr-2 border border-2" style="object-fit:cover">
                                    <img v-else src="@/assets/basket.png" class="rounded-full h-full h-10 mr-2 border border-2">
                                    <div class="flex flex-col">
                                        <span class="font-semibold text-base">{{item.inventory.name}}</span>
                                    </div>
                                </div>
    
                                <!-- RIGHT SIDE -->
                                <div class="flex items-center gap-2">
                                    <div class="flex flex-col items-end">
                                        <span class="font-semibold text-base">₱{{formatPrice(item.amountTotal)}}</span>
                                        <span class="font-medium text-xs text-gray-500">₱{{formatPrice(item.inventory.sellingPrice)}}/item</span>
                                    </div>
                                    <div class="cursor-pointer">
                                        <i @click="removeItem(index)" class="fa-solid fa-circle-xmark text-red-400"></i>
                                    </div>
                                </div>
                            </div>
                        </TransitionGroup>
                    </div>

                    <!-- DISCOUNT -->
                    <transition name="slide-fade-3">
                        <div v-if="discountOpen" class="flex flex-row px-5 pt-2 pb-4 items-center justify-between w-full">
                            <div class="form-group">
                                <label for="">Discount in Peso</label>
                                <div class="input-group">
                                    <div class="input-group-prepend">
                                        <span class="input-group-text">₱</span>
                                    </div>
                                    <input @focus="$event.target.select()" v-model="order.discount" type="number" min="0" class="input-group-control" placeholder="Enter Discount">
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="">Discount in Percent</label>
                                <div class="input-group">
                                    <div class="input-group-prepend">
                                        <span class="input-group-text"><i class="fa-solid fa-percent"></i></span>
                                    </div>
                                    <input readonly @focus="$event.target.select()" v-model="order.discountPercent" type="number" step="0.01" min="0" class="input-group-control" placeholder="Enter Discount">
                                </div>
                            </div>
                        </div>
                    </transition>


                    <div @click="toggleOpenDiscount" class="z-10 flex flex-0 px-5 py-2 cursor-pointer text-gray-500 font-semibold transition hover:text-gray-600 select-none gap-2 hover:bg-gray-100">
                        <span><i class="fa-solid fa-percent"></i></span>
                        <span>Add Discount +</span>
                    </div>

                    <!-- TOTALS -->
                    <div class="flex flex-0 flex-col px-5 py-2 font-semibold gap-2">
                        <!-- DISCOUNT TOTAL -->
                        <div class="flex justify-between mb-2">
                            <span>Discount</span>
                            <span>₱{{formatPrice(order.discount)}}</span>
                        </div>

                        <!-- SENIOR CITIZEN STATUS -->
                        <div class="flex justify-between items-center mb-2">
                            <span>Senior Citizen/PWD Status</span>
                            <div class="flex flex-row items-center justify-center">
                                <transition name="list">
                                    <input v-if="order.senior" v-model="order.seniorID" type="text" class="form-control h-8 mr-2" placeholder="ID Number">
                                </transition>
                                <button @click="toggleSenior" :class=" order.senior ? 'btn-sm-primary' : 'btn-sm-warning'">
                                    {{order.senior ? 'On': 'Off'}}
                                </button>
                            </div>
                        </div>

                        <!-- SUBTOTAL -->
                        <div class="flex justify-between">
                            <span>Sub-Total</span>
                            <span>₱{{formatPrice(order.subTotal)}}</span>
                        </div>

                        <!-- VAT EXEMPT -->
                        <div class="flex justify-between text-xs">
                            <span>VAT Exempt</span>
                            <span>₱{{formatPrice(order.vatExempt)}}</span>
                        </div>

                        <!-- VAT -->
                        <div class="flex justify-between text-xs">
                            <span>VAT (12%)</span>
                            <span>₱{{formatPrice(order.vat)}}</span>
                        </div>

                        <!-- NET -->
                        <div class="flex justify-between text-xs mb-2">
                            <span>Net</span>
                            <span>₱{{formatPrice(order.net)}}</span>
                        </div>

                        <!-- TOTAL -->
                        <div class="flex justify-between mb-2 text-xl font-bold">
                            <span>Total</span>
                            <span>₱{{formatPrice(order.total)}}</span>
                        </div>

                        <!-- PAYMENT -->
                        <div class="flex justify-between">
                            <span>Payment</span>
                            <span>₱{{formatPrice(order.payInput)}}</span>
                        </div>

                        <!-- CHANGE -->
                        <div class="flex justify-between">
                            <span>Change</span>
                            <span v-if="order.change >= 0" class="text-green-500">₱{{formatPrice(order.change)}}</span>
                            <span v-else class="text-red-500">₱{{formatPriceIntl(order.change)}}</span>
                        </div>
                    </div>

                    <!-- BUTTONS -->
                    <div class="mt-2 flex w-full">
                        <div @click="toggleModal('salesReview')" class="gap-2 cursor-pointer py-4 flex w-full transition items-center justify-center bg-red-400 rounded-bl-xl font-bold text-lg text-red-100 hover:bg-red-500 hover:text-red-200">
                            <i class="fa-solid fa-cash-register"></i>
                            <span>Sell</span>
                        </div>

                        <div @click="toggleModal('modal1')"
                            class="gap-2 cursor-pointer py-4 flex w-full transition items-center justify-center bg-green-500 rounded-br-xl font-bold text-lg text-green-100 hover:bg-green-600 hover:text-green-200">
                            <i class="fa-solid fa-money-bill-wave"></i>
                            <span>Payment</span>
                        </div>
                    </div>
                </div>


                <!-- RIGHT PANE -->
                <div class="flex flex-initial w-full flex-col bg-white rounded-xl shadow-2xl relative overflow-hidden overflow-y-auto"
                    id="child">
                    <!-- TOP -->
                    <div class="px-5 py-5 flex flex-row justify-between items-center sticky top-0 menu-item-header">
                        <!-- LEFT -->
                        <div class="flex flex-row items-center gap-5">
                            <span class="font-black text-4xl" v-if="selectedCategory" :style="{'color': getCategoryColor()}">{{toUpperCase(getCategoryName())}}</span>
                            <span class="font-black text-4xl" v-else>ALL</span>
                        </div>

                        <!-- RIGHT -->
                        <div class="flex flex-row items-center gap-5">
                            <select v-model='selectedCategory' name="" id="" class="form-control w-auto">
                                <option value="" selected>All</option>
                                <option v-for="item in categories" :value="item.id">{{item.name}}</option>
                            </select>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fa-solid fa-magnifying-glass"></i></span>
                                </div>
                                <input v-model="search" @focus="$event.target.select()" type="text" class="input-group-control" placeholder="Search">
                            </div>
                        </div>
                    </div>

                    <!-- BOTTOM -->
                    <div class="px-5 mb-5 flex flex-wrap mt-5 gap-8 gap-y-16 ">
                        <MenuItem v-if="!loading" :title="item.name" v-for="item in searchInventory" @click="addToOrder(item)">
                            <template v-slot:image>
                                <template v-if="item.image">
                                    <img :src="getBaseURL() + item.image" class="select-none" alt="">
                                </template>
                            </template>
                            <template v-slot:name>{{item.name}}</template>
                            <template v-slot:code>{{item.code}}</template>
                            <template v-slot:price>₱{{formatPrice(item.sellingPrice)}}</template>
                        </MenuItem>

                        <LoadingMenuItem v-else/>
                    </div>
                </div>
            </div>
        </Transition>
    </div>
    <!-- MODALS HERE -->

    <!-- MODAL 1 -->
    <Modal ref="modal1" @close="toggleModal('modal1')">
        <template v-slot:body>
            <PaymentInput @close="toggleModal('modal1')" :payInput="formatPrice(order.payInput)" :total="formatPrice(order.total)" :change="(order.change)" @addNumber="addNumber" @addBill="addBill" @deleteNum="deleteNum" @AC='AC' />
        </template>
    </Modal>

    <!-- MODAL 2 -->
    <Modal ref="editItem" @close="toggleModal('editItem')">
        <template v-slot:header>
            <div class="relative flex items-center p-6 bg-white rounded-t-xl min-w-[24rem] overflow-hidden" :style="[invModal.inventory.image ? {'background': 'url(' + getBaseURL() + invModal.inventory.image + ')', 'background-position':'center center', 'background-size':'cover'} : {'background': 'white'}]">
                <div class="flex z-10 w-fit flex-col rounded-lg p-3 backdrop-blur-white">
                    <span class="font-extrabold text-2xl">{{invModal.inventory.name}}</span>
                    <span class="font-extrabold text-sm text-gray-700">{{invModal.inventory.code}}</span>
                </div>
                <i @click="toggleModal('editItem')" class="absolute fa-solid fa-circle-xmark top-0 right-1 transition cursor-pointer text-red-400 hover:text-red-400 text-2xl"></i>
            </div>
        </template>

        <template v-slot:body>
            <div class="flex flex-col gap-6 overflow-hidden bg-gray-100">
                <div class="px-6 py-5 flex flex-col gap-4">
                    <div class="form-group">
                        <label for="">Quantity</label>
                        <input @focus="$event.target.select()" v-model="invModal.qty" type="number" min="1" class="form-control" placeholder="Enter Quantity">
                    </div>

                    <div class="flex flex-col rounded-lg bg-gray-200 p-3 font-bold w-full">
                        <span class="text-gray-400">Total Amount</span>
                        <span class="text-2xl">₱{{formatPrice(invModal.amountTotal)}}</span>
                    </div>
                </div>
            </div>
        </template>
            <div class="modal-submit-button-primary mt-2" @click="toggleModal('editItem')">
                Confirm
            </div>
        <template v-slot:footer>
            
        </template>
    </Modal>

    <!-- MODAL 3 -->
    <Modal ref='addCustomer' @close="toggleModal('addCustomer')">
        <template v-slot:header>
            <div class="flex justify-between items-center gap-8 px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <div class="flex flex-row gap-4 items-center">
                    <span>Add Customer</span>
                    <div class="grid grid-cols-2 divide-x my-shadow-thin overflow-hidden rounded-lg text-sm">
                        <div class="px-4 py-2 cursor-pointer hover:bg-gray-100 active:bg-gray-200 select-none" @click="activateTemporaryCustomerStatus">
                            Temporary
                        </div>
                        <div class="px-4 py-2 cursor-pointer hover:bg-gray-100 active:bg-gray-200 select-none" @click="deactivateTemporaryCustomerStatus">
                            Existing
                        </div>
                    </div>
                </div>
                <span @click="toggleModal('addCustomer')">
                    <i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
                </span>
            </div>
        </template>
        <template v-slot:body>
            <div class="px-6 py-4 flex flex-col gap-4">
                <div class="form-group" v-if="temporaryCustomerStatus">
                    <label for="">Enter Temporary Customer's Name <span class="ml-2 text-sky-500 cursor-pointer" @click="toggleInfoStatus"><i class="fa-solid fa-circle-info"></i></span></label>
                    <span class="mb-2 select-none" v-if="infoStatus">Temporary Customers are not saved in the database.</span>
                    <input @focus="$event.target.select()" v-model="order.temporaryCustomer" type="text" class="form-control" placeholder="Enter Customer Name">
                </div>
                <div class="form-group" v-else>
                    <label for="">Select Existing Customer</label>
                    <select v-model='order.existingCustomer' name="" id="" class="form-control">
                        <option value="" selected disabled>Select a Customer</option>
                        <option v-for="cus in customers" :value="cus.id">{{cus.name}}</option>
                    </select>
                </div>
            </div>
            <button class="modal-submit-button-primary" type="button" @click="toggleModal('addCustomer')">
                Confirm
            </button>
        </template>

    </Modal>

    <!-- MODAL 4 -->
    <Modal ref="salesReview" @close="toggleModal('salesReview')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Review Invoice</span>
                <span @click="toggleModal('salesReview')"><i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i></span>
            </div>
        </template>

        <template v-slot:body>
            <div class="flex flex-col divide-y font-semibold">
                <!-- INVOICE NUM AND DATE -->
                <div class="flex flex-col px-3 py-3">
                    <div class="flex flex-row justify-between gap-20">
                        <span>Invoice # {{order.code}}</span>
                        <span class="text-gray-400">{{time}}</span>
                    </div>
                    <div class="flex flex-row justify-end">
                        <span class="text-gray-400" v-if="order.existingCustomer || order.temporaryCustomer">{{this.order.temporaryCustomer ? this.order.temporaryCustomer : getCustomerName(this.order.existingCustomer)}}</span>
                        <span class="text-red-400" v-else>Walk-in Customer</span>
                    </div>
                </div>


                <!-- ITEMS -->
                <div class="px-3 py-3 flex flex-col pb-10 bg-white">
                    <div class="mb-3">
                        <span class="text-xl font-bold">Items</span>
                    </div>

                    <div class="flex flex-col gap-4">
                        <div class="flex flex-row justify-between gap-8" v-for='item in order.items'>
                            <!-- QTY AND NAME -->
                            <div class="flex flex-row gap-2">

                                <div class="rounded-full bg-sky-400 h-6 w-6 -top-2 left-6 flex items-center justify-center text-sm font-bold text-white">
                                    <span>{{item.qty}}</span>
                                </div>
                                
                                <span>{{item.inventory.name}}</span>
                            </div>
                            <!-- AMOUNT -->
                            <div>
                                <span>₱{{formatPrice(item.amountTotal)}}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- CALCS -->
                <div class="px-3 py-3 flex flex-col bg-white">
                    <!-- DISCOUNT -->
                    <div class="flex flex-row justify-between mb-6">
                        <div class="flex flex-row gap-2">
                            <span>Discount</span>
                        </div>
                        <!-- AMOUNT -->
                        <div>
                            <span>₱{{formatPrice(order.discount)}}</span>
                        </div>
                    </div>

                    <!-- SUBTOTAL -->
                    <div class="flex flex-row justify-between text-lg font-bold mb-3">
                        <div class="flex flex-row gap-2">
                            <span>Sub-Total</span>
                        </div>
                        <!-- AMOUNT -->
                        <div>
                            <span>₱{{formatPrice(order.subTotal)}}</span>
                        </div>
                    </div>

                    <!-- VAT EXEMPT -->
                    <div class="flex flex-row justify-between text-xs">
                        <div class="flex flex-row gap-2">
                            <span>VAT Exempt</span>
                        </div>
                        <!-- AMOUNT -->
                        <div>
                            <span>₱{{formatPrice(order.vatExempt)}}</span>
                        </div>
                    </div>

                    <!-- VAT -->
                    <div class="flex flex-row justify-between text-xs">
                        <div class="flex flex-row gap-2">
                            <span>VAT</span>
                        </div>
                        <!-- AMOUNT -->
                        <div>
                            <span>₱{{formatPrice(order.vat)}}</span>
                        </div>
                    </div>

                    <!-- TOTAL -->
                    <div class="flex flex-row justify-between text-xl font-bold my-6">
                        <div class="flex flex-row gap-2">
                            <span>TOTAL</span>
                        </div>
                        <!-- AMOUNT -->
                        <div>
                            <span>₱{{formatPrice(order.total)}}</span>
                        </div>
                    </div>

                    <!-- PAYMENT -->
                    <div class="flex flex-row justify-between">
                        <div class="flex flex-row gap-2">
                            <span>Payment</span>
                        </div>
                        <!-- AMOUNT -->
                        <div>
                            <span>₱{{formatPrice(order.payInput)}}</span>
                        </div>
                    </div>

                    <!-- CHANGE -->
                    <div class="flex flex-row justify-between text-xl font-bold">
                        <div class="flex flex-row gap-2">
                            <span>Change</span>
                        </div>
                        <!-- AMOUNT -->
                        <div>
                            <span v-if="order.change > 1000" class="text-orange-500">₱{{formatPriceIntl(order.change)}}</span>
                            <span v-else-if="order.change >= 0" class="text-green-500">₱{{formatPrice(order.change)}}</span>
                            <span v-else class="text-red-500">₱{{formatPriceIntl(order.change)}}</span>
                        </div>
                    </div>
                </div>
            </div>
        </template>

        <template v-slot:footer>
            <div @click="submitSales" class="modal-submit-button-primary select-none">
                <div class="gap-2 flex justify-center items-center">
                    <i class="fa-solid fa-cash-register"></i>
                    <span>Confirm Sales</span>
                </div>
            </div>
        </template>
    </Modal>
</template>

<script>
    import Nav from '@/components/Nav.vue'
    import {mixins} from '@/mixins/mixins.js'
    import PaymentInput from '@/components/PaymentInput.vue'
    import Modal from '@/components/Modal.vue'
    import MenuItem from '@/components/MenuItem.vue'
    import { getAPI } from '@/axios-api'
    import LoadingMenuItem from '@/components/LoadingMenuItem.vue'

    export default{
        mixins: [
            mixins
        ],
        components: {
            PaymentInput,
            Nav,
            Modal,
            MenuItem,
            LoadingMenuItem
        },

        data(){
            return{
                config:{
                    headers: {
                        Authorization: `Bearer ${this.$store.state.accessToken}`
                    },
                },
                loading: false, 
                time: null,
                infoStatus: false,
                selectedCategory: '',
                search: '',
                customers: [],
                inventoryAll: [],
                categories: [],
                temporaryCustomerStatus: true,
                order: {
                    existingCustomer: '',
                    temporaryCustomer: '',
                    senior: false,
                    seniorID: '',
                    code: '',
                    items: [],
                    discount: 0,
                    discountPercent: 0,
                    vatExempt: 0,
                    vat: 0,
                    net: 0,
                    total: 0,
                    subTotal: '',

                    payInput: '',
                    change: 0,
                },

                discountOpen: false,

                invModal:{
                    inventory: {
                        id: null,
                        code: '',
                        name: '',
                        unitCost: null,
                        image: '',
                        category: null,
                        sellingPrice: null
                    },
                    qty: 0,
                    amountTotal: 0,
                },
            }
        },

        computed: {
            subTotal(){
                return this.order.items.map(item=>item.amountTotal)
            },

            payInput(){
                return this.order.payInput
            },

            senior(){
                return this.order.senior
            },

            inventories(){
                if(this.selectedCategory){
                    return this.inventoryAll.filter(item => item.category == this.selectedCategory)
                }else{
                    return this.inventoryAll
                }
            },

            searchInventory() {
                return this.inventories.filter(item => {
                    return item.name.toLowerCase().includes(this.search.toString().toLowerCase()) || item.code.toLowerCase().includes(this.search.toString().toLowerCase())
                })
            },

            items(){
                return this.order.items
            },

            discount(){
                return this.order.discount
            },

            discountPercent(){
                return this.order.discountPercent
            },
        },
        

        watch: {
            subTotal(){
                this.watchers()
            },

            discount(){
                this.watchers()
                this.order.discountPercent = ((Number(this.order.discount) / Number(this.order.subTotal)) * 100).toFixed(2)
            },

            // discountPercent(){
            //     this.watchers()
            //     setTimeout(()=>{
            //         this.order.discount = (Number(this.order.discountPercent) / 100) * Number(this.order.subTotal)
            //     }, 1000)
            // },

            payInput(){
                this.order.change = Number(this.payInput) - Number(this.order.total)
            },

            senior(){
                this.watchers()
            },

            items: {
                deep: true,

                handler(){
                    this.updateAmountTotal()
                }
            }
        },



        methods: {
            getCustomers(){
                getAPI.get('/customers/', this.config)
                .then(res=>{
                    this.customers = res.data
                })
            },

            getLatestSales(){
                getAPI.get('/latest-sales-code/', this.config)
                .then(res=>{
                    this.order.code = res.data
                })
            },

            getCategories(){
                getAPI.get('/categories/', this.config)
                .then(res=>{
                    this.categories = res.data
                })
            },

            async getInventories(){
                return getAPI.get('/inventory/', this.config)
                .then(res=>{
                    this.inventoryAll = res.data
                })
            },

            onload(){
                this.getCustomers()
                this.getCategories()
                this.getInventories()
                this.getLatestSales()
            },

            watchers(){
                if(this.order.senior){
                    this.order.subTotal = Number(this.subTotal.reduce((a,b)=>Number(a)+Number(b),0)) / 1.12
                    this.order.vat = 0
                    this.order.vatExempt = Number(this.subTotal.reduce((a,b)=>Number(a)+Number(b),0)) / 1.12 * .12
                    this.order.discount = this.order.subTotal * 0.2
                    this.order.total = Number(this.order.subTotal) - Number(this.order.discount)
                    this.order.net = Number(this.order.total)
                    this.order.change = Number(this.payInput) - Number(this.order.total)
                    return
                }
                this.order.subTotal = Number(this.subTotal.reduce((a,b)=>Number(a)+Number(b),0))
                this.order.total = Number(this.order.subTotal) - Number(this.order.discount)
                this.order.vat = Number(this.order.total) / 1.12 * .12
                this.order.net = Number(this.order.total) - Number(this.order.vat)
                this.order.change = Number(this.payInput) - Number(this.order.total)
                this.order.vatExempt = 0
            },

            editItem(item){
                this.toggleModal('editItem')
                this.invModal = item
            },

            checkIfTwoDecimalPlaces(){
                // return false if over two decimal places
                // return true if less than two decimal places
                if(this.order.payInput.split('.').length > 1){
                    if(this.order.payInput.split('.')[1].length > 1){
                        return false
                    }
                }
                return true
            },

            assertSingleDecimalPoint(){
                // return true if there is a single decimal point in the number
                // return false if there is none
                if(this.order.payInput.split('.').length > 1){
                    return true
                }
                return false
            },

            addNumber(num){
                if (!this.checkIfTwoDecimalPlaces()){
                    return
                }
                if (num == '.' && this.assertSingleDecimalPoint()){
                    return
                }
                this.order.payInput = String(this.order.payInput.concat(num))
            },

            addBill(num){
                this.order.payInput = String(Number(this.order.payInput) + Number(num))
            },

            deleteNum(){
                this.order.payInput = String(this.order.payInput.slice(0, -1))
            },

            // ALL CLEAR
            AC(){
                this.order.payInput = ''
            },

            removeItem(index){
                this.order.items.splice(index, 1)
            },

            customAddItem(code){
                // add item to order
                // if item already in order, increase qty
                // if item not in order, add item
                let itemInOrder = this.order.items.find(item=>item.inventory.code == code)
                if (itemInOrder){
                    itemInOrder.qty++
                    itemInOrder.amountTotal = Number(itemInOrder.inventory.sellingPrice) * Number(itemInOrder.qty)
                }
                else{
                    this.order.items.push({
                        inventory: {
                            name: 'Bruh',
                            code: 'bruh-001',
                            sellingPrice: '500',
                            image: '',
                        },
                        qty: 1,
                        amountTotal: '500',
                    })
                }
            },

            addToOrder(inventoryItem){
                let itemInOrder = this.order.items.find(item=>item.inventory.code == inventoryItem.code)
                if(itemInOrder){
                    itemInOrder.qty++
                    itemInOrder.amountTotal = Number(itemInOrder.inventory.sellingPrice) * Number(itemInOrder.qty)
                } else {
                    this.order.items.push({
                        inventory: inventoryItem,
                        qty: 1,
                        amountTotal: Number(inventoryItem.sellingPrice) * 1,
                    })
                }
            },

            updateAmountTotal(){
                this.order.items.forEach(item=>{
                    item.amountTotal = Number(item.inventory.sellingPrice) * Number(item.qty)
                })
            },

            deductItem(index){
                // if qty is 1, remove item
                // if qty is greater than 1, decrease qty
                if (this.order.items[index].qty == 1){
                    this.removeItem(index)
                }
                else{
                    this.order.items[index].qty--
                    this.order.items[index].amountTotal = Number(this.order.items[index].inventory.sellingPrice) * Number(this.order.items[index].qty)
                }
            },

            capitalize(str){
                return str.charAt(0).toUpperCase() + str.slice(1)
            },

            toggleSenior(){
                if(this.order.senior){
                    this.order.discount = 0
                    this.order.discountPercent = 0
                    this.order.seniorID = ''
                }
                this.order.senior = !this.order.senior
            },

            getBaseURL(){
                return getAPI.defaults.baseURL
            },
            getCategoryName(){
                return this.categories.find(item=>item.id == this.selectedCategory).name
            },
            getCategoryColor(){
                return this.categories.find(item=>item.id == this.selectedCategory).color
            },

            toggleOpenDiscount(){
                this.discountOpen = !this.discountOpen
            },

            activateTemporaryCustomerStatus(){
                this.temporaryCustomerStatus = true
                this.order.existingCustomer = ''
            },

            deactivateTemporaryCustomerStatus(){
                this.temporaryCustomerStatus = false
                this.order.temporaryCustomer = ''
            },

            toggleInfoStatus(){
                this.infoStatus = !this.infoStatus
            },

            getCustomerName(id){
                return this.customers.find(item=>item.id == id).name
            },

            resetData(){
                this.order = {
                    items: [],
                    subTotal: 0,
                    vat: 0,
                    vatExempt: 0,
                    discount: 0,
                    discountPercent: 0,
                    total: 0,
                    net: 0,
                    change: 0,
                    payInput: '',
                    existingCustomer: '',
                    temporaryCustomer: '',
                    senior: false,
                    discountOpen: false,
                    infoStatus: false,
                    temporaryCustomerStatus: false,
                }

                this.infoStatus = false,
                this.selectedCategory = '',
                this.search = '',
                this.temporaryCustomerStatus = true,
                this.discountOpen = false,
                this.invModal = {
                    inventory: {
                        id: null,
                        code: '',
                        name: '',
                        unitCost: null,
                        image: '',
                        category: null,
                        sellingPrice: null
                    },
                    qty: 0,
                    amountTotal: 0,
                }
                this.getLatestSales()
            },

            liveTime(){
                const months = [
                    'Jan',
                    'Feb',
                    'Mar',
                    'Apr',
                    'May',
                    'Jun',
                    'Jul',
                    'Aug',
                    'Sep',
                    'Oct',
                    'Nov',
                    'Dec'
                ]

                const days = [
                    'Sun',
                    'Mon',
                    'Tue',
                    'Wed',
                    'Thu',
                    'Fri',
                    'Sat'
                ]
                let value = new Date()
                let year = value.getFullYear()
                let month = months[value.getMonth()]
                let date = value.getDate()
                let hour = (value.getHours() + 24) % 12 || 12; 
                let minute = (value.getMinutes()<10?'0':'') + value.getMinutes()
                let meridian = value.getHours() >= 12 ? 'pm' : 'am'
                let formatted = `${month}. ${date}, ${year} - ${hour}:${minute} ${meridian}`

                this.time = formatted
            },

            createReceipt(id){
                const route = this.$router.resolve('/receipt/' + id);
                window.open(route.href, '_blank');
            },

            submitSales(){
                // ADD A LOADING SCREEN
                this.swalLoading('Saving...', 'Please wait while we save your sales...')

                // SAVE THE ORDER
                setTimeout(()=>{
                    if(this.order.change < 0){
                        this.swalWarning("Change is less than ₱0.00. Please check your payment.")
                    } 
                    else if(this.order.payInput < this.order.total){
                        this.swalWarning("Payment is less than Total. Please check your payment.")
                    }
                    else if(this.items.length == 0){
                        this.swalWarning("No items in the order. Please add items to the order.")
                    } 
                    else {
                        getAPI.post('/sales/', this.order, this.config)
                        .then(res=>{
                            this.swalSuccess('Invoice saved successfully.')
                            this.toggleModal('salesReview')
                            this.resetData()
                            this.onload()
                            this.createReceipt(res.data)
                        })
                        .catch(err=>{
                            this.swalError(err.message)
                            console.log(err)
                        })
                    }
                }, 1000)
            }
        },

        async mounted(){
            this.getCustomers()
            this.getCategories()
            this.getInventories()
            this.getLatestSales()

            this.loading = true
            await this.getInventories()
            this.loading = false

            setInterval(()=>{
                this.liveTime()
            }, 1000);
        }
    }

</script>