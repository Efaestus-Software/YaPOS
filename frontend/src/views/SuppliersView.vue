<template>

    <Nav />

    <Transition name="fade" appear>
        <div class="xl:container xl:px-0 sm:px-4 mx-auto flex flex-col">
            <!-- TITLE -->
            <div class="mb-8 mt-3">
                <span class="font-black text-3xl">SUPPLIERS</span>
            </div>

            <VueTable class="mb-8" enableSearch="true" @toggle="toggle" :data="items" :header="['Name', 'Address', 'Contact', 'Email']" :dataIncluded="['name', 'address', 'contact', 'email']" :enableLink='true' :loading="loading">
                <template v-slot:buttons>
                    <div class="flex flex-row gap-2">
                        <button class="btn-warning my-shadow" @click="toggleModal('addSupplier')">Add New Supplier</button>
                        <button class="btn-success my-shadow" @click="toggleModal('importSuppliers')"><i class="fa-solid fa-file-excel"></i> Import Suppliers</button>
                    </div>
                </template>
            </VueTable>
        </div>
    </Transition>

    <!-- MODAL 1 -->
    <AddSupplierModal ref="addSupplier" @close="toggleModal('addSupplier')" @success="success()" @fail="fail()" />

    <!-- MODAL 2 -->
    <Modal ref="importSuppliers" @close="toggleModal('importSuppliers')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Import Supplier</span>
                <span @click="toggleModal('importSuppliers')">
                    <i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
                </span>
            </div>
        </template>

        <template v-slot:body>
            <form @submit.prevent="submitImportSuppliers()">
                <div class="px-6 py-4 flex flex-col gap-4">
                    <!-- MAIN BODY -->
                    <div class="form-group">
                        <label for="">Select an Excel File</label>
                        <input @change="importSuppliersOnChange()" ref="importSuppliersFile" type="file" class="block w-full text-sm text-slate-500
                        file:mr-4 file:py-2 file:px-4
                        file:rounded-full file:border-0
                        file:text-sm file:font-semibold
                        file:bg-green-300 file:text-green-900
                        file:transition
                        hover:file:bg-green-400" accept=".xlsx, .xls">
                    </div>
                    <a class="link font-medium" :href="getBaseURL() + '/static/files/YaPOS Add Suppliers.xlsx'">Download Excel Template</a>
                </div>
                <button class="modal-submit-button-success" type="submit">
                    Import
                </button>
            </form>
        </template>
    </Modal>

    <!-- MODAL 2.5 -->
    <modal ref="partyDetails" @close="toggleModal('partyDetails')">
        <template v-slot:header>
            <div class="relative flex items-center p-6 bg-white rounded-t-xl min-w-[48rem]">
                <div class="flex flex-row gap-4 items-center">
                    <span class="font-extrabold text-2xl">Supplier Details</span>
                    <span class="link font-medium" @click="editSupplierModal">Edit Supplier</span>
                </div>
                <i @click="toggleModal('partyDetails')" class="absolute fa-solid fa-circle-xmark top-0 right-1 transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
            </div>
        </template>

        <template v-slot:body>
            <div class="bg-white flex flex-col gap-6 rounded-b-xl">
                <div class="grid grid-cols-2 gap-y-8 px-6 py-5 bg-gray-100 rounded-b-xl">
                    <div>
                        <label class="font-bold text-gray-400">Name</label><br>
                        <span class="font-extrabold text-xl" v-if="partyDetails.name">{{partyDetails.name}}</span>
                    </div>
                    <div>
                        <label class="font-bold text-gray-400">Address</label><br>
                        <span class="font-extrabold text-xl" v-if="partyDetails.address">{{partyDetails.address}}</span>
                    </div>
                    <div>
                        <label for="" class="font-bold text-gray-400">Phone</label><br>
                        <span class="font-extrabold text-xl">{{partyDetails.contact}}</span>
                    </div>
                    <div>
                        <label for="" class="font-bold text-gray-400">Email</label><br>
                        <span class="font-extrabold text-xl">{{partyDetails.email}}</span>
                    </div>
                </div>
            </div>
        </template>
    </modal>

    <!-- MODAL 3 -->
    <modal ref="editParty" @close="toggleModal('editParty')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Edit Customer</span>
                <span @click="toggleModal('editParty')">
                    <i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
                </span>
            </div>
        </template>

        <template v-slot:body>
            <form @submit.prevent="submitEditParty">
                <div class="px-6 py-4 flex flex-col gap-4">
                    <!-- MAIN BODY -->
                    <div class="flex flex-row gap-4">
                        <div class="form-group">
                            <label for="">Name</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fa-solid fa-user"></i></span>
                                </div>
                                <input v-model="editParty.name" type="text" class="input-group-control" placeholder="Enter Customer's Name" required>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="">Address</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fa-solid fa-location-dot"></i></span>
                                </div>
                                <input v-model="editParty.address" type="text" class="input-group-control" placeholder="Enter Customer's Address">
                            </div>

                        </div>
                    </div>

                    <div class="flex flex-row gap-4">
                        <div class="form-group">
                            <label for="">Contact</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fa-solid fa-phone"></i></span>
                                </div>
                                <input v-model="editParty.contact" type="tel" class="input-group-control" placeholder="Enter Customer's Contact Number">
                            </div>

                        </div>
                        <div class="form-group">
                            <label for="">Email</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fa-solid fa-at"></i></span>
                                </div>
                                <input v-model="editParty.email" type="email" class="input-group-control" placeholder="Enter Customer's Email">
                            </div>

                        </div>
                    </div>
                </div>
                <button class="modal-submit-button-primary" type="submit">
                    Save
                </button>
            </form>
        </template>
    </modal>
</template>

<script>

import Nav from '@/components/Nav.vue'
import SubNav from '@/components/SubNav.vue'
import { mixins } from '@/mixins/mixins.js'
import VueTable from '@/components/VueTable.vue'
import { getAPI } from '@/axios-api'
import Modal from '@/components/Modal.vue'
import AddSupplierModal from '@/components/AddSupplierModal.vue'

export default {
    mixins: [
        mixins
    ],
    components: {
    Nav,
    SubNav,
    VueTable,
    Modal,
    AddSupplierModal
},

    data() {
        return {
            config:{
                headers: {
                    Authorization: `Bearer ${this.$store.state.accessToken}`
                }
            },

            loading: true,

            items: [],

            addParty: {
                name: '',
                address: '',
                contact: '',
                email: ''
            },

            editParty: {
                name: '',
                address: '',
                contact: '',
                email: ''
            },
            
            partyDetails: {
                name: '',
                address: '',
                contact: '',
                email: ''
            },

            import: {
                file: '',
            }
        }
    },

    methods: {
        toggle(id){
            this.toggleModal('partyDetails')
            this.partyDetails = this.items.find(item=>item.id == id)
        },

        editSupplierModal(){
            this.editParty = {...this.partyDetails}
            this.toggleModal('editParty')
        },

        submitEditParty(){
            getAPI.put(`/suppliers/${this.editParty.id}/`, this.editParty, this.config)
            .then(res=>{
                this.$swal({
                    buttonsStyling: false,
                    customClass: {
                        confirmButton: 'btn-primary',
                        cancelButton: 'btn btn-danger',
                    },
                    title: 'Success',
                    text: 'Supplier Updated',
                    icon: 'success',
                    button: 'OK'
                })
                this.toggleModal('editParty')
                this.toggleModal('partyDetails')
                this.clearAll()
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
        },

        clearAll(){
            this.addParty = {
                name: '',
                address: '',
                contact: '',
                email: ''
            }

            this.editParty = {
                name: '',
                address: '',
                contact: '',
                email: ''
            }

            this.partyDetails = {
                name: '',
                address: '',
                contact: '',
                email: ''
            }
        },

        importSuppliersOnChange(){
            this.import.file = this.$refs.importSuppliersFile.files[0]
        },

        submitImportSuppliers(){
            const formData = new FormData()
            formData.append('file', this.import.file)
            getAPI.post('/import-supplier-excel/', formData, this.config)
            .then(response => {
                this.$swal({
                    buttonsStyling: false,
                    customClass: {
                        confirmButton: 'btn-primary',
                        cancelButton: 'btn btn-danger',
                    },
                    title: 'Success',
                    text: 'Suppliers Added',
                    icon: 'success',
                    button: 'OK'
                })
                this.toggleModal('importSuppliers')
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
        },

        async onload(){
            return getAPI.get('suppliers', this.config).then(res => {
                this.items = res.data
            })
        },

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
            this.onload()
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

        getBaseURL(){
            return getAPI.defaults.baseURL
        }
    },

    async mounted(){
        this.loading = true
        await this.onload()
        this.loading = false
    }
}

</script>