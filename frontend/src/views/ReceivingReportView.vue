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

            <form class="flex flex-col mb-8 bg-white rounded-2xl w-full shadow-xl" @submit.prevent="submitReceivingReport">
                <!-- TITLE -->
                <div class="font-bold text-2xl px-5 pt-5 pb-3">
                    Create a Receiving Report
                </div>

                <!-- CODE AND DATE -->
                <div class="flex flex-row justify-between items-center px-5">
                    <!-- CODE -->
                    <div class="flex gap-4 items-center">
                        <div class="rounded-lg bg-gray-100 p-3  font-extrabold text-2xl" v-if="!loading">
                            {{order.code}}
                        </div>
                        <div class="rounded-lg bg-gray-100 p-3  font-extrabold text-2xl" v-else>
                            Loading...
                        </div>
                        <select v-model="order.suppliers" name="" id="" class="form-control w-64" required>
                            <option value="" selected disabled>Select Supplier</option>
                            <option v-for="supplier in suppliers" :value="supplier.id" >{{supplier.name}}</option>
                        </select>

                        <div @click="toggleModal('addSupplier')" class="cursor-pointer text-yellow-500 hover:text-yellow-600" title="Add Supplier">
                            <i class="fa-solid fa-circle-plus text-2xl"></i>
                        </div>
                    </div>

                    <!-- DATE -->
                    <div>
                        <div class="rounded-lg bg-gray-100 p-3 font-extrabold text-2xl">
                            {{toUpperCase(formatDate(order.date))}}
                        </div>
                    </div>
                </div>

                <!-- BODY -->
                <div class="flex flex-col m-5 p-6 bg-gray-100 rounded-lg">
                    <!-- COL HEADER -->
                    <div class="grid grid-rows-1 grid-cols-12 gap-4 font-bold">
                        <div class="col-span-2 ">Category</div>
                        <div class="col-span-4 ">Item Code - Name</div>
                        <div class="col-span-1">Remaining</div>
                        <div class="col-span-2">Unit Cost</div>
                        <div class="col-span-1">Quantity</div>
                        <div class="col-span-2 ">Total</div>
                    </div>

                    <!-- INPUTS -->
                    <TransitionGroup name="list">
                        <div v-for="(item, index) in order.items" class="grid grid-rows-1 grid-cols-12 gap-4 my-1 relative"
                            :key="item">
                            <!-- 1 -->
                            <div class="col-span-2">
                                <select v-model="item.category" @change="filterInventory(item.category, index)" name="" id="" class="form-control" required>
                                    <option value="-1" selected disabled>None</option>
                                    <option value="">All</option>
                                    <option v-for="category in categories" :value="category.id">{{category.name}}</option>
                                </select>
                            </div>
                            <!-- 2 -->
                            <div class="col-span-4">
                                <select @change="getInvDetails(index)" v-model="item.inventory" name="" id="" class="form-control" required>
                                    <option value="" selected disabled>None</option>
                                    <option v-for="inventory in item.invList" :value="inventory.id">{{inventory.code}} - {{inventory.name}}</option>
                                </select>
                            </div>
                            <!-- 3 -->
                            <div class="col-span-1">
                                <input v-model="item.remaining" readonly type="number" class="form-control">
                            </div>
                            <!-- 4 -->
                            <div class="input-group col-span-2">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">₱</span>
                                </div>
                                <input :value="formatPrice(item.unitCost)" readonly type="text" class="input-group-control">
                            </div>
                            <!-- 5 -->
                            <div class="col-auto col-span-1">
                                <input @input="getAmountTotal(index)" v-model="item.qty" type="number" class="form-control" min="0" required>
                            </div>
                            <!-- 6 -->
                            <div class="input-group col-span-2">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">₱</span>
                                </div>
                                <input readonly type="text" class="input-group-control" :value="formatPrice(item.amountTotal)">
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
                <div class="flex flex-row items-center justify-end px-6 pb-3">
                    <div class="flex flex-col rounded-lg bg-gray-100 p-3 font-bold w-64">
                        <span class="text-gray-400">Total Cost</span>
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
    <!-- MODAL 1 -->
    <AddSupplierModal ref="addSupplier" @close="toggleModal('addSupplier')" @success="success()" @fail="fail()" />
</template>

<script>
    import { getAPI } from '@/axios-api'
    import Nav from '@/components/Nav.vue'
    import SubNav from '@/components/SubNav.vue'
    import { mixins } from '@/mixins/mixins.js'
    import AddSupplierModal from '@/components/AddSupplierModal.vue'
    export default{
        mixins: [
            mixins
        ],
        components:{
            Nav,
            SubNav,
            AddSupplierModal
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
                    amountTotal: null,
                    suppliers: '',
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
                suppliers: []
            }
        },

        computed:{
            sumItemsAmountTotal(){
                return this.order.items.map(item=>item.amountTotal)
            },
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
                if(id){
                    this.order.items[index].invList = this.inventories.filter(item=>item.category==id)
                    this.order.items[index].inventory = ''
                } else {
                    this.order.items[index].invList = this.inventories
                }
            },

            async getInvDetails(index){
                return getAPI.get(`/inventory/${this.order.items[index].inventory}/`, this.config)
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

            async getLatestRRCode(){
                return getAPI.get('/latest-rr-code/', this.config)
                .then(res=>{
                    this.order.code = res.data
                })
            },

            async getSuppliers(){
                return getAPI.get('/suppliers/', this.config)
                .then(res=>{
                    this.suppliers = res.data
                })
            },

            async onload(){
                this.getCategories()
                this.getInventories()
                this.getSuppliers()
            },

            addNewLine(){
                this.order.items.push({
                    category: -1,
                    inventory: '',
                    remaining: null,
                    unitCost: null,
                    qty: null,
                    amountTotal: 0,
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

            clearReceivingReport(){
                this.order.suppliers = ''
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
                this.swalLoading('Saving...', 'Please wait while we save the receiving report')

                setTimeout(()=>{
                    // delete all invList from items
                    this.order.items.forEach(item=>{
                        delete item.invList
                    })
                    getAPI.post('/receiving-report/', this.order, this.config)
                    .then(res=>{
                        this.$swal({
                            buttonsStyling: false,
                            customClass: {
                                confirmButton: 'btn-primary',
                                cancelButton: 'btn btn-danger',
                            },
                            title: 'Success',
                            text: 'Receiving report added',
                            icon: 'success',
                            button: 'OK'
                        })
                        this.clearReceivingReport()
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
            this.loading = true
            await this.getLatestRRCode()
            this.loading = false
            this.onload()
            
        }
    }
</script>