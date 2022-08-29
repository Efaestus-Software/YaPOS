<template>
    <Nav />
    <SubNav>
        <template v-slot:body>
            <router-link to="/inventory" id="sub-inventory">Products</router-link>
            <router-link to="/inventory-list" id="sub-inventory-list">List</router-link>
        </template>
    </SubNav>
    <Transition name="fade" appear>
        <div class="xl:container xl:px-0 sm:px-4 mx-auto flex flex-col mb-4">
            <!-- TITLE -->
            <div class="mb-8">
                <span class="font-black text-3xl">INVENTORY</span>
            </div>

            <!-- BODY -->
            <InvVueTable @toggle="toggle" :data="list" :header="['Code', 'Name', 'Qty', 'Selling Price', 'Unit Cost']" :enableSearch="true">
                <template v-slot:buttons>
                    <div class="flex flex-row gap-2">
                        <button class="btn-warning my-shadow" @click="toggleModal('addItemModal')">Add New Item</button>
                        <button class="btn-success my-shadow" @click="toggleModal('importItems')"><i class="fa-solid fa-file-excel"></i> Import Items</button>
                    </div>
                </template>
            </InvVueTable>
        </div>
    </Transition>

    <!-- MODAL 1 -->
    <Modal ref="invDetailsModal" @close="toggleModal('invDetailsModal')">
        <template v-slot:header>
            <div class="relative flex items-center p-6 bg-white rounded-t-xl min-w-[48rem] overflow-hidden" :style="[invModal.image ? {'background': 'url(' + getBaseURL() + invModal.image + ')', 'background-position':'center center', 'background-size':'cover'} : {'background': 'white'}]">
                <div class="flex z-10 w-fit flex-col rounded-lg p-3 backdrop-blur-white">
                    <span class="font-extrabold text-2xl">{{invModal.name}}</span>
                    <span class="font-extrabold text-sm text-gray-700">{{invModal.code}}</span>
                </div>
                <i @click="toggleModal('invDetailsModal')" class="absolute fa-solid fa-circle-xmark top-0 right-1 transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
            </div>
        </template>

        <template v-slot:body>
            <div class="bg-white flex flex-col gap-6 rounded-b-xl overflow-hidden">
                <div class="grid grid-cols-2 gap-y-8 px-6 py-5 bg-gray-100">
                    <div>
                        <label class="font-bold text-gray-400">Quantity Remaining</label><br>
                        <span class="font-extrabold text-xl" v-if="invModal.qty">{{invModal.qty}}</span>
                    </div>
                    <div>
                        <label class="font-bold text-gray-400">Selling Price</label><br>
                        <span class="font-extrabold text-xl" v-if="invModal.sellingPrice">₱{{formatPrice(invModal.sellingPrice)}}</span>
                    </div>
                    <div>
                        <label for="" class="font-bold text-gray-400">Unit Cost</label><br>
                        <span class="font-extrabold text-xl">₱{{formatPrice(invModal.unitCost)}}</span>
                    </div>
                </div>
            </div>
        </template>
    </Modal>

    <!-- MODAL 2 -->
    <Modal ref="addItemModal" @close="toggleModal('addItemModal')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Add Item</span>
                <span @click="toggleModal('addItemModal')"><i
                        class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i></span>
            </div>
        </template>
        <template v-slot:body>
            <div class="px-6 py-4 flex flex-col gap-8">
                <!-- MAIN BODY -->
                <TransitionGroup name="list">
                    <div v-for="(item, index) in addItem" :key="item"
                        class="flex flex-row gap-4 bg-white p-4 rounded-xl shadow-md relative">
                        <i @click="toggleRemoveItem(index)"
                            class="z-10 fa-solid fa-circle-xmark cursor-pointer text-red-400 absolute -top-2 -right-2 text-xl"></i>
                        <!-- ADD IMAGE -->
                        <div class="flex flex-col relative">
                            <input type="file" :id="'imageInput' + index" @change="onFileChange($event, index)" hidden>
                            <div v-if="!item.imageURL" @click="chooseFile(`imageInput${index}`)" class="select-none rounded-md outline-2 outline-dashed outline-gray-400 w-48 h-48 flex items-center justify-center text-gray-400 cursor-pointer font-bold relative">
                                + Add image
                            </div>
                            <img v-if="item.imageURL" @click="chooseFile(`imageInput${index}`)" :src="item.imageURL" alt="" class="w-48 h-48 rounded-md" style="object-fit: cover">
                            <div @click="removeImage(index)" v-if="item.imageURL" class="cursor-pointer text-center rounded-b-md bottom-0 absolute w-full bg-black/50 text-white">
                                <span class="font-semibold opacity-100 hover:text-gray-400">Remove Image</span>
                            </div>
                        </div>

                        <!-- NAME AND PRICE -->
                        <div class="flex flex-col justify-between">
                            <div class="form-group">
                                <label for="">Name</label>
                                <input v-model="item.name" type="text" class="form-control" placeholder="Enter item name">
                            </div>

                            <div class="form-group">
                                <label for="">Selling Price</label>
                                <div class="input-group">
                                    <div class="input-group-prepend">
                                        <span class="input-group-text">₱</span>
                                    </div>
                                    <input v-model="item.sellingPrice" type="number" step="0.01" class="input-group-control"
                                        placeholder="Enter price">
                                </div>
                            </div>
                        </div>

                        <!-- CODE AND UNIT COST -->
                        <div class="flex flex-col justify-between">
                            <div class="form-group">
                                <label for="">Code</label>
                                <input v-model="item.code" type="text" class="form-control" placeholder="Enter item code">
                            </div>
                            <div class="form-group">
                                <label for="">Unit Cost</label>
                                <div class="input-group">
                                    <div class="input-group-prepend">
                                        <span class="input-group-text">₱</span>
                                    </div>
                                    <input v-model="item.unitCost" type="number" step="0.01" class="input-group-control"
                                        placeholder="Enter Unit Cost">
                                </div>
                            </div>
                        </div>

                        <!-- QTY AND CAT -->
                        <div class="flex flex-col justify-between">

                            <div class="form-group">
                                <label for="">Quantity</label>
                                <input v-model="item.qty" type="number" class="form-control" placeholder="Enter Quantity" min="0">
                            </div>
                            <div class="form-group">
                                <label for="">Category</label>
                                <select v-model="item.category" name="" id="" class="form-control">
                                    <option value="" selected disabled>Select Category</option>
                                    <option v-for="category in categories" :value="category.id">{{category.name}}</option>
                                </select>
                            </div>
                        </div>


                        <!-- REMOVE STATUS -->
                        <Transition>
                            <div v-if="item.removeStatus"
                                class="absolute top-0 left-0 w-full h-full rounded-xl flex flex-col items-center justify-center"
                                style="backdrop-filter: blur(10px); background-color: rgba(0,0,0,0.6);">
                                <div class="font-bold text-2xl text-red-400">
                                    <i class="fa-solid fa-trash-can mr-2"></i> Remove item?
                                </div>
                                <div class="flex gap-4 mt-2">
                                    <button class="btn-danger shadow-md" @click="removeItem(index)">Remove</button>
                                    <button class="btn shadow-md" @click="cancelRemoveItem(index)">Cancel</button>
                                </div>
                            </div>
                        </Transition>
                    </div>
                </TransitionGroup>

                <!-- ADD ITEM -->
                <div @click="addNewItem"
                    class="select-none py-4 flex outline-2 outline-dashed outline-gray-400 items-center justify-center text-gray-400 rounded-lg cursor-pointer font-bold hover:outline-gray-800 hover:text-gray-800">
                    <span class="mx-5">+ Add new item</span>
                </div>
            </div>
        </template>
        <template v-slot:footer>
            <div class="modal-submit-button-primary" @click="submitAddItems()">
                Save
            </div>
        </template>
    </Modal>

    <!-- MODAL 3 -->
    <Modal ref="importItems" @close="toggleModal('importItems')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Import Items</span>
                <span @click="toggleModal('importItems')">
                    <i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
                </span>
            </div>
        </template>

        <template v-slot:body>
            <form @submit.prevent="submitImportItems()">
                <div class="px-6 py-4 flex flex-col gap-4">
                    <!-- MAIN BODY -->
                    <div class="form-group">
                        <label for="">Select an Excel File</label>
                        <input @change="importItemsOnChange()" ref="importItemsFile" type="file" class="block w-full text-sm text-slate-500
                        file:mr-4 file:py-2 file:px-4
                        file:rounded-full file:border-0
                        file:text-sm file:font-semibold
                        file:bg-green-300 file:text-green-900
                        file:transition
                        hover:file:bg-green-400" accept=".xlsx, .xls">
                    </div>
                    <a class="link font-medium" :href="getBaseURL() + '/static/files/YaPOS Add Items.xlsx'">Download Excel Template</a>
                </div>
                <button class="modal-submit-button-success" type="submit">
                    Import
                </button>
            </form>
        </template>
    </Modal>
    <!-- <pre>{{$data}}</pre> -->
</template>

<script>
import Nav from '@/components/Nav.vue'
import MenuItem from '@/components/MenuItem.vue'
import AddMenuItem from '@/components/AddMenuItem.vue'
import Modal from '@/components/Modal.vue'
import SubNav from '../components/SubNav.vue'
import { mixins } from '@/mixins/mixins.js'
import { getAPI } from '@/axios-api'
import InvVueTable from '@/components/InvVueTable.vue'
import AddInventoryModal from '../components/AddInventoryModal.vue'

export default{
    mixins: [
        mixins
    ],

    components: {
    Nav,
    MenuItem,
    AddMenuItem,
    Modal,
    SubNav,
    InvVueTable,
    AddInventoryModal
},

    data(){
        return{
            config:{
                headers: {
                    Authorization: `Bearer ${this.$store.state.accessToken}`
                }
            },
            list: [{
                code: '',
                name: '',
                qty: '',
                sellingPrice: '',
                unitCost: '',
                image: '',
                category: '',
                id: '',
            }],

            categories: [],

            invModal: {
                id: '',
                code: '',
                name: '',
                qty: '',
                sellingPrice: '',
                unitCost: '',
                image: '',
                category: '',
            },

            import: {
                file: '',
            },

            addItem: [
                {
                    image: null,
                    imageURL: null,
                    name: '',
                    sellingPrice: null,
                    unitCost: null,
                    qty: null,
                    code: '',
                    removeStatus: false,
                    category: ''
                },
            ]
        }
    },

    methods: {
        importItemsOnChange(){
            this.import.file = this.$refs.importItemsFile.files[0]
        },
        getBaseURL(){
            return getAPI.defaults.baseURL
        },

        submitImportItems(){
            const formData = new FormData()
            formData.append('file', this.import.file)
            this.swalLoading('Importing Items', 'Please wait while we import your items')
            setTimeout(()=>{
                getAPI.post('/import-items-excel/', formData, this.config)
                .then(res => {
                    this.$swal({
                        buttonsStyling: false,
                        customClass: {
                            confirmButton: 'btn-primary',
                            cancelButton: 'btn btn-danger',
                        },
                        title: 'Success',
                        text: 'Items Added',
                        icon: 'success',
                        button: 'OK'
                    })
                    this.toggleModal('importItems')
                    this.onload()
                })
                .catch(error => {
                    this.$swal({
                        buttonsStyling: false,
                        customClass: {
                            confirmButton: 'btn-primary',
                            cancelButton: 'btn btn-danger',
                        },
                        title: 'Error',
                        text: error.message,
                        icon: 'error',
                        button: 'OK'
                    })
                    console.log(error)
                })
            }, 1000)
        },

        getInventory(){
            getAPI('/inventory', this.config)
            .then(res => {
                this.list = res.data
            })
        },

        getCategories(){
            getAPI('/categories', this.config)
            .then(res => {
                this.categories = res.data
            })
        },

        onload(){
            this.getInventory()
            this.getCategories()
        },

        toggle(id){
            this.toggleModal('invDetailsModal')
            this.invModal = this.list.find(item=>item.id == id)
        },

        toggleModal(id){
            this.$refs[id].showModal = !this.$refs[id].showModal
        },
        
        removeImage(index){
            this.addItem[index].image = null
            this.addItem[index].imageURL = null
        },

        chooseFile(id){
            document.getElementById(id).click()
        },

        onFileChange(e, index){
            const file = e.target.files[0];
            this.addItem[index].imageURL = URL.createObjectURL(file);
            this.addItem[index].image = file;
        },

        removeItem(index){
            this.addItem.splice(index, 1)
        },

        toggleRemoveItem(index){
            this.addItem[index].removeStatus = !this.addItem[index].removeStatus
        },

        cancelRemoveItem(index){
            this.addItem[index].removeStatus = false
        },

        addNewItem(){
            this.addItem.push({
                image: null,
                imageURL: null,
                name: null,
                price: null,
                qty: null,
                code: null,
                removeStatus: false,
                category: ''
            })
        },

        clearAddItem(){
            this.addItem = [
                {
                    image: null,
                    imageURL: null,
                    name: '',
                    sellingPrice: null,
                    unitCost: null,
                    qty: null,
                    code: '',
                    removeStatus: false,
                    category: ''
                },
            ]
        },

        submitAddItems(){
            const formData = new FormData()
            this.addItem.forEach(item => {
                if(item.image){
                    formData.append('image', item.image)
                }
                formData.append('name', item.name)
                formData.append('sellingPrice', item.sellingPrice)
                formData.append('unitCost', item.unitCost)
                formData.append('qty', item.qty)
                formData.append('code', item.code)
                formData.append('category', item.category)
                formData.append('imageURL', item.imageURL)
            })
            getAPI.post('/inventory/', formData, this.config)
            .then(res=>{
                this.$swal({
                    buttonsStyling: false,
                    customClass: {
                        confirmButton: 'btn-primary',
                        cancelButton: 'btn btn-danger',
                    },
                    title: 'Success',
                    text: 'Item added',
                    icon: 'success',
                    button: 'OK'
                })
                this.toggleModal('addItemModal')
                this.clearAddItem()
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
        },
    },

    mounted(){
        this.onload()
    },
}
</script>