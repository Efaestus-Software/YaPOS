<template>

    <Nav />
    
    <Transition name="fade" appear>
        <div class="xl:container xl:px-0 sm:px-4 mx-auto flex flex-col">
            <!-- TITLE -->
            <div class="mb-8 mt-3">
                <span class="font-black text-3xl">CUSTOMERS</span>
            </div>

            <CustomerVueTable @toggle="customerDetailsModal" :loading="loading" :data="list" :header="['Name', 'Address', 'Contact', 'Email']" :enableSearch="true">
                <template v-slot:buttons>
                    <div class="flex flex-row gap-2">
                        <button class="btn-warning my-shadow" @click="toggleModal('addCustomer')">Add New Customer</button>
                        <button class="btn-success my-shadow" @click="toggleModal('importCustomers')"><i class="fa-solid fa-file-excel"></i> Import Customers</button>
                    </div>
                </template>
            </CustomerVueTable>
        </div>
    </Transition>

    <!-- MODAL 1 -->
    <Modal ref="addCustomer" @close="toggleModal('addCustomer')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Add Customer</span>
                <span @click="toggleModal('addCustomer')">
                    <i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
                </span>
            </div>
        </template>

        <template v-slot:body>
            <form @submit.prevent="submitCustomer">
                <div class="px-6 py-4 flex flex-col gap-4">
                    <!-- MAIN BODY -->
                    <div class="flex flex-row gap-4">
                        <div class="form-group">
                            <label for="">Name</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fa-solid fa-user"></i></span>
                                </div>
                                <input v-model="addCustomer.name" type="text" class="input-group-control" placeholder="Enter Customer's Name" required>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="">Address</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fa-solid fa-location-dot"></i></span>
                                </div>
                                <input v-model="addCustomer.address" type="text" class="input-group-control" placeholder="Enter Customer's Address">
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
                                <input v-model="addCustomer.contact" type="tel" class="input-group-control" placeholder="Enter Customer's Contact Number">
                            </div>

                        </div>
                        <div class="form-group">
                            <label for="">Email</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fa-solid fa-at"></i></span>
                                </div>
                                <input v-model="addCustomer.email" type="email" class="input-group-control" placeholder="Enter Customer's Email">
                            </div>

                        </div>
                    </div>
                </div>
                <button class="modal-submit-button-primary" type="submit">
                    Save
                </button>
            </form>
        </template>
    </Modal>

    <!-- MODAL 2 -->
    <Modal ref="importCustomers" @close="toggleModal('importCustomers')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Import Customer</span>
                <span @click="toggleModal('importCustomers')">
                    <i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
                </span>
            </div>
        </template>

        <template v-slot:body>
            <form @submit.prevent="submitImportCustomer()">
                <div class="px-6 py-4 flex flex-col gap-4">
                    <!-- MAIN BODY -->
                    <div class="form-group">
                        <label for="">Select an Excel File</label>
                        <input @change="importCustomerOnChange()" ref="importCustomerFile" type="file" class="block w-full text-sm text-slate-500
                        file:mr-4 file:py-2 file:px-4
                        file:rounded-full file:border-0
                        file:text-sm file:font-semibold
                        file:bg-green-300 file:text-green-900
                        file:transition
                        hover:file:bg-green-400" accept=".xlsx, .xls">
                    </div>
                    <a class="link font-medium" :href="getBaseURL() + '/static/files/YaPOS Add Customers.xlsx'">Download Excel Template</a>
                </div>
                <button class="modal-submit-button-success" type="submit">
                    Import
                </button>
            </form>
        </template>
    </Modal>

    <!-- MODAL 2.5 -->
    <modal ref="customerDetails" @close="toggleModal('customerDetails')">
        <template v-slot:header>
            <div class="relative flex items-center p-6 bg-white rounded-t-xl min-w-[48rem]">
                <div class="flex flex-row gap-4 items-center">
                    <span class="font-extrabold text-2xl">Customer Details</span>
                    <span class="link font-medium" @click="editCustomerModal">Edit Customer</span>
                </div>
                <i @click="toggleModal('customerDetails')" class="absolute fa-solid fa-circle-xmark top-0 right-1 transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
            </div>
        </template>

        <template v-slot:body>
            <div class="bg-white flex flex-col gap-6 rounded-b-xl">
                <div class="grid grid-cols-2 gap-y-8 px-6 py-5 bg-gray-100 rounded-b-xl">
                    <div>
                        <label class="font-bold text-gray-400">Name</label><br>
                        <span class="font-extrabold text-xl" v-if="customerDetails.name">{{customerDetails.name}}</span>
                    </div>
                    <div>
                        <label class="font-bold text-gray-400">Address</label><br>
                        <span class="font-extrabold text-xl" v-if="customerDetails.address">{{customerDetails.address}}</span>
                    </div>
                    <div>
                        <label for="" class="font-bold text-gray-400">Phone</label><br>
                        <span class="font-extrabold text-xl">{{customerDetails.contact}}</span>
                    </div>
                    <div>
                        <label for="" class="font-bold text-gray-400">Email</label><br>
                        <span class="font-extrabold text-xl">{{customerDetails.email}}</span>
                    </div>
                </div>
            </div>
        </template>
    </modal>

    <!-- MODAL 3 -->
    <modal ref="editCustomer" @close="toggleModal('editCustomer')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Edit Customer</span>
                <span @click="toggleModal('editCustomer')">
                    <i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i>
                </span>
            </div>
        </template>

        <template v-slot:body>
            <form @submit.prevent="submitEditCustomer">
                <div class="px-6 py-4 flex flex-col gap-4">
                    <!-- MAIN BODY -->
                    <div class="flex flex-row gap-4">
                        <div class="form-group">
                            <label for="">Name</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fa-solid fa-user"></i></span>
                                </div>
                                <input v-model="editCustomer.name" type="text" class="input-group-control" placeholder="Enter Customer's Name" required>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="">Address</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fa-solid fa-location-dot"></i></span>
                                </div>
                                <input v-model="editCustomer.address" type="text" class="input-group-control" placeholder="Enter Customer's Address">
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
                                <input v-model="editCustomer.contact" type="tel" class="input-group-control" placeholder="Enter Customer's Contact Number">
                            </div>

                        </div>
                        <div class="form-group">
                            <label for="">Email</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fa-solid fa-at"></i></span>
                                </div>
                                <input v-model="editCustomer.email" type="email" class="input-group-control" placeholder="Enter Customer's Email">
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
import CustomerVueTable from '@/components/CustomerVueTable.vue'
import { getAPI } from '@/axios-api'
import Modal from '@/components/Modal.vue'

export default {
    mixins: [
        mixins
    ],
    components: {
        Nav,
        SubNav,
        VueTable,
        CustomerVueTable,
        Modal,
    },

    data() {
        return {
            config:{
                headers: {
                    Authorization: `Bearer ${this.$store.state.accessToken}`
                }
            },
            loading: false,
            list: [{
                name: '',
                address: '',
                contact: '',
                email: '',
            }],

            addCustomer: {
                name: '',
                address: '',
                contact: '',
                email: '',
            },

            customerDetails: {
                name: '',
                address: '',
                contact: '',
                email: '',
            },

            editCustomer: {
                name: '',
                address: '',
                contact: '',
                email: '',
            },

            import: {
                file: '',
            }
        }
    },

    methods: {
        editCustomerModal(){
            this.toggleModal('editCustomer')
            this.editCustomer = {...this.customerDetails}
        },
        customerDetailsModal(e){
            this.toggleModal('customerDetails')
            this.customerDetails = this.list.find(item=>item.id == e)
        },
        importCustomerOnChange(){
            this.import.file = this.$refs.importCustomerFile.files[0]
        },

        submitImportCustomer(){
            const formData = new FormData()
            formData.append('file', this.import.file)
            getAPI.post('/import-customer-excel/', formData, this.config)
            .then(response => {
                this.$swal({
                    buttonsStyling: false,
                    customClass: {
                        confirmButton: 'btn-primary',
                        cancelButton: 'btn btn-danger',
                    },
                    title: 'Success',
                    text: 'Customers Added',
                    icon: 'success',
                    button: 'OK'
                })
                this.toggleModal('importCustomers')
                this.getCustomers()
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

        async getCustomers(){
            return getAPI('/customers', this.config)
            .then(response => {
                this.list = response.data
            })
        },
        
        clearAddCustomer(){
            this.addCustomer = {
                name: '',
                address: '',
                contact: '',
                email: '',
            }
        },

        clearEditCustomer(){
            this.editCustomer = {
                name: '',
                address: '',
                contact: '',
                email: '',
            }
        },

        clearCustomerDetails(){
            this.customerDetails = {
                name: '',
                address: '',
                contact: '',
                email: '',
            }
        },

        async onload(){
            return this.getCustomers()
        },

        submitEditCustomer(){
            getAPI.put(`/customers/${this.editCustomer.id}/`, this.editCustomer, this.config)
            .then(response => {
                this.$swal({
                    buttonsStyling: false,
                    customClass: {
                        confirmButton: 'btn-primary',
                        cancelButton: 'btn btn-danger',
                    },
                    title: 'Success',
                    text: 'Customer Updated',
                    icon: 'success',
                    button: 'OK'
                })
                this.toggleModal('editCustomer')
                this.toggleModal('customerDetails')
                this.clearAddCustomer()
                this.clearCustomerDetails()
                this.clearEditCustomer()
                this.getCustomers()
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

        submitCustomer(){
            this.swalLoading('Saving...', 'Please wait while we are saving your customer')

            setTimeout(()=>{
                getAPI.post('/customers/', this.addCustomer, this.config)
                .then(res=>{
                    this.$swal({
                        buttonsStyling: false,
                        customClass: {
                            confirmButton: 'btn-primary',
                            cancelButton: 'btn btn-danger',
                        },
                        title: 'Success',
                        text: 'Customer Added',
                        icon: 'success',
                        button: 'OK'
                    })
                    this.clearAddCustomer()
                    this.clearCustomerDetails()
                    this.clearEditCustomer()
                    this.onload()
                    this.toggleModal('addCustomer')
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

        getBaseURL(){
            return getAPI.defaults.baseURL
        }
    },

    async mounted(){
        this.loading = true
        await this.getCustomers()
        this.loading = false
    }

}

</script>