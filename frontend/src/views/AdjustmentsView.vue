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

            <form class="flex flex-col bg-white mb-8 rounded-2xl w-full shadow-xl" @submit.prevent="submitReceivingReport()">
                <!-- TITLE -->
                <div class="font-bold text-2xl px-5 pt-5 pb-3">
                    Create an Adjustment
                </div>

                <!-- CODE AND DATE -->
                <div class="flex flex-row justify-between items-center px-5 font-extrabold text-2xl">
                    <!-- CODE -->
                    <div class="rounded-lg bg-gray-100 p-3" v-if="!loading">
                        {{order.code}}
                    </div>
                    <div class="rounded-lg bg-gray-100 p-3" v-else>
                        Loading...
                    </div>

                    <!-- DATE -->
                    <div class="rounded-lg bg-gray-100 p-3">
                        {{toUpperCase(formatDate(order.date))}}
                    </div>
                </div>

                <!-- BODY -->
                <div class="flex flex-col m-5 p-6 bg-gray-100 rounded-lg">
                    <!-- COL HEADER -->
                    <div class="grid grid-rows-1 grid-cols-12 gap-4 font-bold">
                        <div class="col-span-2 ">Category</div>
                        <div class="col-span-3 ">Item Code - Name</div>
                        <div class="col-span-2">Remaining</div>
                        <div class="col-span-2">Unit Cost</div>
                        <div class="col-span-1">Quantity</div>
                        <div class="col-span-2 ">Lost</div>
                    </div>

                    <!-- INPUTS -->
                    <TransitionGroup name="list">
                        <div v-for="(item, index) in order.items" class="grid grid-rows-1 grid-cols-12 gap-4 my-1 relative"
                            :key="item">
                            <!-- 1 -->
                            <div class="col-span-2">
                                <select v-model="item.category" @change="filterInventory(item.category, index)" name="" id="" class="form-control">
                                    <option value="-1" selected disabled>None</option>
                                    <option value="">All</option>
                                    <option v-for="category in categories" :value="category.id">{{category.name}}</option>
                                </select>
                            </div>
                            <!-- 2 -->
                            <div class="col-span-3">
                                <select @change="getInvDetails(index)" v-model="item.inventory" name="" id="" class="form-control" required>
                                    <option value="" selected disabled>None</option>
                                    <option v-for="inventory in item.invList" :value="inventory.id">{{inventory.code}} - {{inventory.name}}</option>
                                </select>
                            </div>
                            <!-- 3 -->
                            <div class="col-span-2">
                                <input v-model="item.remaining" type="text" class="form-control" @keypress="validate" readonly>
                            </div>
                            <!-- 4 -->
                            <div class="input-group col-span-2">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">₱</span>
                                </div>
                                <input :value="formatPrice(item.unitCost)" type="text" class="input-group-control" @keypress="validate" readonly>
                            </div>
                            <!-- 5 -->
                            <div class="col-auto col-span-1">
                                <input @input="getAmountTotal(index)" v-model="item.qty" type="number" min="0" :max="item.remaining" class="form-control" required>
                            </div>
                            <!-- 6 -->
                            <div class="input-group col-span-2">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">₱</span>
                                </div>
                                <input type="text" class="input-group-control" :value="formatPrice(item.amountTotal)" readonly>
                            </div>
                            <!-- ELLIPSIS -->
                            <div @click="removeSpecificLine(index)"
                                class="transition absolute -right-5 rounded-md hover:text-red-500 h-full flex items-center justify-center w-4 cursor-pointer">
                                <i class="fa-solid fa-xmark"></i>
                            </div>
                        </div>
                    </TransitionGroup>

                    <!-- ADD REMOVE -->
                    <div class="py-4 flex flex-row gap-2">
                        <button type="button" class="btn-warning" @click="addNewLine()">+ Add line</button>
                        <button type="button" class="btn-danger" @click="removeLine()">- Remove line</button>
                    </div>
                </div>

                <!-- TYPE AND TOTAL -->
                <div class="flex flex-row items-center justify-between px-6 pb-3">
                    <div class="form-group">
                        <label for="">Type of Adjustment</label>
                        <select v-model="order.type" name="" id="" class="form-control" required>
                            <option value="" selected disabled>None</option>
                            <option value="Spoilage">Spoilage</option>
                            <option value="Others">Others</option>
                        </select>
                    </div>
                    <div class="flex flex-col rounded-lg bg-gray-100 p-3 font-bold w-64">
                        <span class="text-gray-400">Total Lost</span>
                        <span class="text-2xl">₱{{formatPrice(order.amountTotal)}}</span>
                    </div>
                </div>

                <!-- SAVE -->
                <button type="submit" class="modal-submit-button-primary mt-2">
                    Save
                </button>
            </form>

        </div>
    </Transition>
</template>

<script>
    import { getAPI } from '@/axios-api'
    import Nav from '@/components/Nav.vue'
    import SubNav from '@/components/SubNav.vue'
    import { mixins } from '@/mixins/mixins.js'
    export default{
        mixins: [
            mixins
        ],
        components:{
            Nav,
            SubNav
        },

        data(){
            return{
                config:{
                    headers: {
                        Authorization: `Bearer ${this.$store.state.accessToken}`
                    }
                },
                loading: false,
                order: {
                    date: new Date().toISOString().split('T')[0],
                    code: 'null',
                    amountTotal: 0,
                    type: '',
                    items: [
                        {
                            category: '-1',
                            inventory: '',
                            remaining: null,
                            unitCost: null,
                            qty: null,
                            amountTotal: 0,
                            invList: [],
                        }
                    ]
                },

                categories: [],
                inventories: [],
            }
        },

        computed: {
            sumItemsAmountTotal(){
                return this.order.items.map(item=>item.amountTotal)
            }
        },

        watch: {
            sumItemsAmountTotal(){
                this.order.amountTotal = this.sumItemsAmountTotal.reduce((a,b)=>Number(a)+Number(b), 0)
            }
        },

        methods: {
            success(){
                this.$swal({
                    buttonsStyling: false,
                    customClass: {
                        confirmButton: 'btn-primary',
                        cancelButton: 'btn btn-danger',
                    },
                    title: 'Success',
                    text: 'Supplier added',
                    icon: 'success',
                    button: 'OK'
                })
                this.getSuppliers()
            },

            fail(){
                this.$swal({
                    buttonsStyling: false,
                    customClass: {
                        confirmButton: 'btn-primary',
                        cancelButton: 'btn btn-danger',
                    },
                    title: 'Error',
                    text: err.message,
                    icon: 'error',
                    button: 'OK'
                })
                console.log(err)
            },

            filterInventory(id, index){
                console.log(id, index)
                if(id){
                    this.order.items[index].invList = this.inventories.filter(item=>item.category==id)
                    this.order.items[index].inventory = ''
                } else {
                    this.order.items[index].invList = this.inventories
                }
            },

            getInvDetails(index){
                getAPI.get(`/inventory/${this.order.items[index].inventory}/`, this.config)
                .then(res=>{
                    this.order.items[index].remaining = res.data.qty
                    this.order.items[index].unitCost = res.data.unitCost
                })
            },

            getAmountTotal(index){
                let data = this.order.items[index]
                data.amountTotal = Number(data.unitCost) * Number(data.qty)
            },

            async getCategories(){
                return getAPI.get('/categories', this.config).then(res => {
                    this.categories = res.data
                })
            },

            async getInventories(){
                return getAPI.get('/inventory', this.config).then(res => {
                    this.inventories = res.data
                })
            },

            async getLatestADCode(){
                return getAPI.get('/latest-adj-code/', this.config)
                .then(res=>{
                    this.order.code = res.data
                })
            },

            onload(){
                this.getCategories()
                this.getLatestADCode()
                this.getInventories()
            },

            addNewLine(){
                this.order.items.push({
                    category: '-1',
                    inventory: '',
                    remaining: null,
                    unitCost: null,
                    qty: null,
                    amountTotal: 0,
                    invList: [],
                })
            },

            removeSpecificLine(index){
                this.order.items.splice(index, 1)
            },

            removeLine(){
                this.order.items.pop()
            },

            toUpperCase(value){
                return value.toUpperCase()
            },

            clearAdjustment(){
                this.order.type = ''
                this.order.items = [
                    {
                        category: '-1',
                        inventory: '',
                        remaining: null,
                        unitCost: null,
                        qty: null,
                        amountTotal: 0,
                        invList: [],
                    }
                ]
            },

            submitReceivingReport(){
                //add a loading screen
                this.swalLoading('Saving...', 'Please wait while we save the adjustments...')

                setTimeout(()=>{
                    // delete all invList from items
                    this.order.items.forEach(item=>{
                        delete item.invList
                    })
                    getAPI.post('/adjustment/', this.order, this.config)
                    .then(res=>{
                        if (res.data == 1){
                                this.$swal({
                                buttonsStyling: false,
                                customClass: {
                                    confirmButton: 'btn-primary',
                                    cancelButton: 'btn btn-danger',
                                },
                                title: 'Warning',
                                text: 'Some adjustments are not valid. Items with higher qty than the stock are skipped.',
                                icon: 'warning',
                                button: 'OK'
                            })
                        }

                        if (res.data == 2){
                            this.$swal({
                                buttonsStyling: false,
                                customClass: {
                                    confirmButton: 'btn-primary',
                                    cancelButton: 'btn btn-danger',
                                },
                                title: 'Warning',
                                text: 'Total amount is ₱0.00. Please check your adjustments.',
                                icon: 'warning',
                                button: 'OK'
                            })
                        }

                        if (res.data == 0){
                            this.$swal({
                                buttonsStyling: false,
                                customClass: {
                                    confirmButton: 'btn-primary',
                                    cancelButton: 'btn btn-danger',
                                },
                                title: 'Success',
                                text: 'Adjustments saved',
                                icon: 'success',
                                button: 'OK'
                            })
                        }
                        this.clearAdjustment()
                        this.onload()
                    })
                    .catch(err=>{
                        this.$swal({
                            buttonsStyling: false,
                            customClass: {
                                confirmButton: 'btn-primary',
                                cancelButton: 'btn btn-danger',
                            },
                            title: 'Error',
                            text: err.message,
                            icon: 'error',
                            button: 'OK'
                        })
                        console.log(err)
                    })
                }, 1000)
            },
        },

        async mounted(){
            this.getCategories()
            this.getLatestADCode()
            this.getInventories()
            this.loading = true
            await this.getLatestADCode()
            this.loading = false
        }
    }
</script>