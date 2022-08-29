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
            <div class="flex flex-row">
                <!-- LEFT PANE -->
                <div class="flex flex-col flex-none w-1/6">
                    <!-- TITLE AGAIN -->
                    <div class="flex">
                        <span class="font-extrabold text-2xl">Categories</span>
                    </div>

                    <!-- CATEGORY SELECTIONS -->
                    <div class="mt-3 bg-white rounded-2xl shadow-xl flex flex-col overflow-hidden" v-if="!loading">
                        <div @click="changeSelectedCategory(null)"
                            class="select-none cat-btn font-bold border px-5 py-3 hover:bg-gray-100">
                            All
                        </div>
                        <div v-for="category in categories" @click="changeSelectedCategory(category.id)"
                            :style="{color: category.color}" :key="category"
                            class="select-none cat-btn font-bold border px-5 py-3 hover:bg-gray-100">
                            {{category.name}}
                        </div>
                    </div>

                    <div class="mt-3 bg-white rounded-2xl shadow-xl flex flex-col overflow-hidden" v-else>
                        <div class="select-none cat-btn font-bold border px-5 py-3 animate-pulse">
                            <span class="text-gray-400">Loading ...</span>
                        </div>
                    </div>

                    <!-- ADD NEW CAT -->
                    <button @click="toggleModal('addCategoryModal')"
                        class="mt-8 text-gray-400 hover:text-gray-700 rounded-lg px-5 py-2 outline-dashed outline-2 outline-gray-400 transition ease-out hover:outline-gray-700">
                        <span class="font-bold">+ Add new category</span>
                    </button>
                </div>

                <!-- RIGHT PANE -->
                <div class="flex flex-col flex-auto ml-14 ">
                    <!-- TITLE AGAIN -->
                    <div class="flex">
                        <span class="font-extrabold text-2xl">Products</span>
                    </div>

                    <!-- ITEMS -->
                    <div class="mt-3 bg-white shadow-xl rounded-2xl py-5 px-5">
                        <!-- TOP -->
                        <div class="flex flex-row justify-between items-center">
                            <div class="flex items-center"><span class="font-black text-3xl" :style="{color: getCategoryColor(selectedCategory)}">{{toUpperCase(getCategoryName(selectedCategory))}}</span>
                                <i v-if="selectedCategory" @click="toggleEditCategoryModal('editCategoryModal', getCategory(selectedCategory))" class="ml-3 fa-solid fa-pen link" title="Edit Category"></i>
                            </div>

                            <div>
                                <input v-model="search" type="text" class="form-control" placeholder="Search">
                            </div>
                        </div>

                        <!-- ITEM BODY -->
                        <div class="mt-4 flex flew-row flex-wrap gap-9">
                            <AddMenuItem @click="toggleModal('addItemModal')" />

                            <MenuItem v-if="!loading" :title="inventory.name" v-for="inventory in searchInventory" @click="toggleEditModal('editItemModal', inventory)">
                                <template v-slot:image>
                                    <template v-if="inventory.image">
                                        <img :src="getBaseURL() + inventory.image" alt="">
                                    </template>
                                </template>
                                <template v-slot:name>{{inventory.name}}</template>
                                <template v-slot:code>{{inventory.code}}</template>
                                <template v-slot:price>₱{{formatPrice(inventory.sellingPrice)}}</template>
                            </MenuItem>

                            <LoadingMenuItem v-else />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Transition>

    <!-- ADD MODALS HERE -->

    <!-- MODAL 1 -->
    <Modal ref="addCategoryModal" @close="toggleModal('addCategoryModal')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Add Category</span>
                <span @click="toggleModal('addCategoryModal')"><i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i></span>
            </div>
        </template>
        <template v-slot:body>
            <div class="px-6 py-2 w-96">
                <div class="form-group pb-3">
                    <label for="">Category Name</label>
                    <input v-model="addCategoryModal.name" type="text" class="form-control"
                        placeholder="Enter category name">
                </div>

                <div class="form-group pt-3">
                    <label for="">Select Accent Color</label>
                    <input v-model="addCategoryModal.color" type="color" class="form-control">
                </div>
            </div>
        </template>
        <template v-slot:footer>
            <div @click="submitAddCategoryModal()" class="modal-submit-button-primary mt-2">
                Save
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
    <Modal ref="editCategoryModal" @close="toggleModal('editCategoryModal')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Edit Category</span>
                <span @click="toggleModal('editCategoryModal')"><i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i></span>
            </div>
        </template>
        <template v-slot:body>
            <div class="px-6 py-2 w-96">
                <div class="form-group pb-3">
                    <label for="">Category Name</label>
                    <input v-model="editCategory.name" type="text" class="form-control" placeholder="Enter category name">
                </div>

                <div class="form-group pt-3">
                    <label for="">Select Accent Color</label>
                    <input v-model="editCategory.color" type="color" class="form-control">
                </div>
            </div>
        </template>
        <template v-slot:footer>
            <div class="modal-submit-button-primary mt-2" @click="submitEditCategory">
                Save
            </div>
        </template>
    </Modal>

    <!-- MODAL 4 -->
    <Modal ref="editItemModal" @close="toggleModal('editItemModal')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Edit Item</span>
                <span @click="toggleModal('editItemModal')">
                    <i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
                </span>
            </div>
        </template>
        <template v-slot:body>
            <div class="px-6 py-4 flex flex-col gap-8">
                <!-- MAIN BODY -->
                <div class="flex flex-row gap-4 bg-white p-4 rounded-xl shadow-md relative">
                    <!-- ADD IMAGE -->
                    <div class="flex relative flex-col">
                        <input type="file" id="imageInputEdit" @change="onFileChangeEdit($event)" hidden>
                        <div v-if="!editItem.imageURL" @click="chooseFileEdit(`imageInputEdit`)" class="select-none rounded-md outline-2 outline-dashed outline-gray-400 w-48 h-48 flex items-center justify-center text-gray-400 cursor-pointer font-bold">
                            + Add image
                        </div>
                        <img v-if="editItem.imageURL" @click="chooseFileEdit(`imageInputEdit`)" :src="editItem.imageURL" alt="" class="w-48 h-48 rounded-md" style="object-fit: cover">
                        <div @click="removeImageEdit" v-if="editItem.imageURL" class="cursor-pointer text-center rounded-b-md bottom-0 absolute w-full bg-black/50 text-white">
                            <span class="font-semibold opacity-100 hover:text-gray-400">Remove Image</span>
                        </div>
                    </div>
                    
                    <!-- NAME AND PRICE -->
                    <div class="flex flex-col justify-between">
                        <div class="form-group">
                            <label for="">Name</label>
                            <input v-model="editItem.name" type="text" class="form-control" placeholder="Enter item name">
                        </div>
                        <div class="form-group">
                            <label for="">Selling Price</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">₱</span>
                                </div>
                                <input v-model="editItem.sellingPrice" type="number" step="0.01" class="input-group-control" placeholder="Enter price">
                            </div>
                        </div>
                    </div>
                    <!-- CODE AND UNIT COST -->
                    <div class="flex flex-col justify-between">
                        <div class="form-group">
                            <label for="">Code</label>
                            <input v-model="editItem.code" type="text" class="form-control" placeholder="Enter item code">
                        </div>
                        <div class="form-group">
                            <label for="">Unit Cost</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">₱</span>
                                </div>
                                <input v-model="editItem.unitCost" type="number" step="0.01" class="input-group-control" placeholder="Enter Unit Cost">
                            </div>
                        </div>
                    </div>
                    <!-- QTY AND CAT -->
                    <div class="flex flex-col justify-between">
                        <div class="form-group">
                            <label for="">Quantity</label>
                            <input v-model="editItem.qty" type="number" class="form-control" placeholder="Enter Quantity" min="0">
                        </div>
                        <div class="form-group">
                            <label for="">Category</label>
                            <select v-model="editItem.category" name="" id="" class="form-control">
                                <option value="" selected disabled>Select Category</option>
                                <option v-for="category in categories" :value="category.id">{{category.name}}</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
        </template>
        <template v-slot:footer>
            <div class="flex">
                <div class="modal-submit-button-primary rounded-br-none" @click="submitEditItem()">
                    Save
                </div>

                <div class="modal-submit-button-danger rounded-bl-none" @click="deleteItem()">
                    Delete
                </div>
            </div>
        </template>
    </Modal>
</template>

<style scoped>
    .cat-btn{
        cursor: pointer;
    }

    .ease-out{
        transition: 100ms ease-out;
    }
</style>

<script>
    import Nav from '@/components/Nav.vue'
    import MenuItem from '@/components/MenuItem.vue'
    import AddMenuItem from '@/components/AddMenuItem.vue'
    import Modal from '@/components/Modal.vue'
    import SubNav from '../components/SubNav.vue'
    import { mixins } from '@/mixins/mixins.js'
    import { getAPI } from '@/axios-api'
    import LoadingMenuItem from '@/components/LoadingMenuItem.vue'

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
            LoadingMenuItem,
        },

        data(){
            return{
                config:{
                    headers: {
                        Authorization: `Bearer ${this.$store.state.accessToken}`
                    }
                },
                loading: true,
                categories: [],
                inventoryAll: [],
                addCategoryModal: {
                    name: '',
                    color: "#000"
                },

                editCategory:{
                    id: '',
                    name: '',
                    color: ''
                },

                selectedCategory: null,
                search: '',

                editItem: {
                    name: '',
                    code: '',
                    sellingPrice: '',
                    unitCost: '',
                    qty: '',
                    category: '',
                    imageURL: '',
                    removeStatus: false,
                    image: null,
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

        computed:{
            //return inventory filtered by category
            inventories(){
                if(this.selectedCategory){
                    return this.inventoryAll.filter(item => item.category == this.selectedCategory)
                }else{
                    return this.inventoryAll
                }
            },

            //search Inventory with the search bar
            searchInventory() {
                return this.inventories.filter(item => {
                    return item.name.toLowerCase().includes(this.search.toString().toLowerCase()) || item.code.toLowerCase().includes(this.search.toString().toLowerCase())
                })
            },
        },

        methods:{
            async getCategories(){
                return getAPI('/categories', this.config).then(res => {
                    this.categories = res.data
                })
            },
            async getInventory(){
                return getAPI('/inventory', this.config).then(res => {
                    this.inventoryAll = res.data
                })
            },

            onload(){
                this.getCategories()
                this.getInventory()
            },

            removeImage(index){
                this.addItem[index].image = null
                this.addItem[index].imageURL = null
            },

            removeImageEdit(){
                this.editItem.image = null
                this.editItem.imageURL = null
            },

            toggleModal(id){
                this.$refs[id].showModal = !this.$refs[id].showModal
            },

            toggleEditModal(id, item){
                this.editItem = {...item}
                this.editItem.imageURL = item.image ? (getAPI.defaults.baseURL + item.image) : null
                this.editItem.image = null
                this.$refs[id].showModal = !this.$refs[id].showModal
            },

            toggleEditCategoryModal(id, category){
                this.editCategory = category
                this.$refs[id].showModal = !this.$refs[id].showModal
            },

            chooseFile(id){
                document.getElementById(id).click()
            },

            onFileChange(e, index){
                const file = e.target.files[0];
                this.addItem[index].imageURL = URL.createObjectURL(file);
                this.addItem[index].image = file;
            },

            toggleRemoveItem(index){
                this.addItem[index].removeStatus = !this.addItem[index].removeStatus
            },

            cancelRemoveItem(index){
                this.addItem[index].removeStatus = false
            },

            removeItem(index){
                this.addItem.splice(index, 1)
            },

            chooseFileEdit(id){
                document.getElementById(id).click()
            },

            onFileChangeEdit(e){
                const file = e.target.files[0];
                this.editItem.imageURL = URL.createObjectURL(file);
                this.editItem.image = file;
            },

            toggleRemoveItemEdit(){
                this.editItem.removeStatus = !this.editItem.removeStatus
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


            submitAddCategoryModal(){
                getAPI.post('/categories/', this.addCategoryModal, this.config)
                .then(res=>{
                    this.toggleModal('addCategoryModal')
                    this.$swal({
                        buttonsStyling: false,
                        customClass: {
                            confirmButton: 'btn-primary',
                            cancelButton: 'btn btn-danger',
                        },
                        title: 'Success',
                        text: 'Category added',
                        icon: 'success',
                        button: 'OK'
                    })
                    this.getCategories()
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

            toUpperCase(str){
                return str.toUpperCase()
            },
            changeSelectedCategory(category){
                this.selectedCategory = category
            },
            //get name of category by id
            getCategoryName(id){
                try{
                    return this.categories.find(item => item.id == id).name
                }
                catch(err){
                    return 'All'
                }
            },

            getCategoryColor(id){
                try{
                    return this.categories.find(item => item.id == id).color
                }
                catch(err){
                    return '#000'
                }
            },

            getCategory(id){
                return this.categories.find(item => item.id == id)
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

            submitEditItem(){
                const formData = new FormData()
                formData.append('image', this.editItem.image)
                formData.append('name', this.editItem.name)
                formData.append('sellingPrice', this.editItem.sellingPrice)
                formData.append('unitCost', this.editItem.unitCost)
                formData.append('qty', this.editItem.qty)
                formData.append('code', this.editItem.code)
                formData.append('category', this.editItem.category)
                formData.append('imageURL', this.editItem.imageURL)
                getAPI.put(`/inventory/${this.editItem.id}/`, formData, this.config)
                .then(res=>{
                    this.$swal({
                        buttonsStyling: false,
                        customClass: {
                            confirmButton: 'btn-primary',
                            cancelButton: 'btn btn-danger',
                        },
                        title: 'Success',
                        text: 'Item updated',
                        icon: 'success',
                        button: 'OK'
                    })
                    this.toggleModal('editItemModal')
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

            submitEditCategory(){
                getAPI.put(`/category/${this.editCategory.id}/`, this.editCategory, this.config)
                .then(res=>{
                    this.$swal({
                        buttonsStyling: false,
                        customClass: {
                            confirmButton: 'btn-primary',
                            cancelButton: 'btn btn-danger',
                        },
                        title: 'Success',
                        text: 'Category updated',
                        icon: 'success',
                        button: 'OK'
                    })
                    this.toggleModal('editCategoryModal')
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

            getBaseURL(){
                return getAPI.defaults.baseURL
            },

            deleteItem(){
                this.$swal({
                    buttonsStyling: false,
                    customClass: {
                        confirmButton: 'btn-danger ml-2',
                        cancelButton: 'btn',
                    },
                    title: 'Are you sure?',
                    text: "You won't be able to revert this!",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Yes, delete it!',
                    cancelButtonText: 'No, cancel!',
                    reverseButtons: true
                }).then(result=>{
                    if(result.isConfirmed){
                        this.swalLoading('Deleting')
                        setTimeout(()=>{
                            getAPI.delete(`/inventory/${this.editItem.id}`, this.config)
                            .then(res=>{
                                this.swalSuccess('Item Deleted')
                                this.onload()
                                this.toggleModal('editItemModal')
                            })
                            .catch(err=>{
                                this.swalError(err.message)
                            })
                        }, 1000)
                    }
                })
            }

            

        },

        async mounted(){
            this.loading = true
            await this.getCategories()
            await this.getInventory()
            this.loading = false
        }
    }
</script>