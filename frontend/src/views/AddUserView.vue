<template>
    <Nav />
    <SubNav>
        <template v-slot:body>
            <router-link to="/user-settings/" id="sub-user-settings">User Settings</router-link>
            <router-link to="/business-settings/" id="sub-business-settings">Business Settings</router-link>
            <router-link to="/add-user/" id="sub-add-user">Add Users</router-link>
        </template>
    </SubNav>
    
    <Transition name="fade" appear>
        <div class="xl:container xl:px-0 sm:px-4 mx-auto flex flex-col items-center">
            <div class="rounded-2xl bg-white divide-y shadow-xl w-[36rem] mt-6">
                <!-- HEADER -->
                <div class="flex flex-row items-center justify-between font-black text-3xl px-6 py-4">
                    <span>ADD USERS</span>
                    <span @click="toggleModal('addUserModal')" class="cursor-pointer text-yellow-500 hover:text-yellow-600"><i class="fa-solid fa-circle-plus"></i></span>
                </div>

                <!-- BODY -->
                <div class="px-6 py-4 flex flex-col">
                    <!-- TITLE -->
                    <span class="font-bold mb-2">
                        Users
                    </span>

                    <!-- TABLE -->
                    <div @contextmenu.prevent="dude(user.id)" v-for="(user, index) in users" class="flex flex-row font-semibold justify-between rounded-md p-2 -mx-2" :class="index % 2 === 0 ? 'bg-gray-100': ''">
                        <span>{{user.first_name}} {{user.last_name}}</span>
                        <span>
                            <span class="text-gray-500">{{user.username}}</span>
                            <i title="Super User" v-if="user.is_superuser" class="fa-solid fa-user-tie ml-2"></i>
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </Transition>

    <!-- MODAL 1 -->
    <Modal ref="addUserModal" @close="toggleModal('addUserModal')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Add User</span>
                <span @click="toggleModal('addUserModal')"><i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i></span>
            </div>
        </template>

        <template v-slot:body>
            <form class="flex flex-col" @submit.prevent="submitAddUser()">
                <div class="flex flex-col px-6 py-4 gap-4 w-[28rem]">
                    <div class="form-group w-full">
                        <label for="">First Name</label>
                        <input v-model="userModal.first_name" type="text" class="form-control" placeholder="Enter User's First Name">
                    </div>

                    <div class="form-group w-full">
                        <label for="">Last Name</label>
                        <input v-model="userModal.last_name" type="text" class="form-control" placeholder="Enter User's Last Name">
                    </div>
                </div>

                <button class="modal-submit-button-primary" type="submit">
                    Save
                </button>
            </form>
        </template>
    </Modal>
</template>

<script>
import { getAPI } from '@/axios-api'
import Nav from '@/components/Nav.vue'
import SubNav from '@/components/SubNav.vue'
import { mixins } from '@/mixins/mixins.js'
import Modal from '@/components/Modal.vue'

export default{
    components:{
        Nav,
        SubNav,
        Modal
    },

    mixins: [mixins],

    data(){
        return {
            config:{
                headers: {
                    Authorization: `Bearer ${this.$store.state.accessToken}`
                }
            },

            me: {
                id: '',
            },

            users: [],

            userModal: {
                first_name: '',
                last_name: '',
            }
        }
    },

    methods: {
        getUsers(){
            getAPI.get('/users/', this.config)
            .then(res => {
                this.users = res.data
            })
        },

        onload(){
            this.getUsers()
            this.getMe()
        },

        getMe(){
            getAPI.get('/me/', this.config)
            .then(res => {
                this.me = res.data
            })
        },

        submitAddUser(){
            this.swalLoading('Adding User...')
            setTimeout(() => {
                getAPI.post('/add-user/', this.userModal, this.config)
                .then(res => {
                    this.swalSuccess('User Added')
                    this.getUsers()
                    this.toggleModal('addUserModal')
                })
                .catch(err=>{
                    this.swalError(err.message)
                })
            }, 1000)
        },

        dude(id){
            if (id == this.me.id){
                return
            }
            this.$swal({
                buttonsStyling: false,
                customClass: {
                    confirmButton: 'btn-danger mr-2',
                    cancelButton: 'btn',
                },
                title: 'Delete User?',
                text: "Are you sure you want to delete this user?",
                icon: 'warning',
                showConfirmButton: 1,
                showCancelButton: 1,
                confirmButtonText: 'Delete',
                cancelButtonText: "Cancel"
            })
            .then(result=>{
                if (result.isConfirmed){
                    this.swalLoading('Deleting User...')
                    setTimeout(() => {
                        getAPI.delete(`/users/${id}/`, this.config)
                        .then(res => {
                            this.swalSuccess('User Deleted')
                            this.getUsers()
                        })
                        .catch(err=>{
                            this.swalError(err.message)
                        })
                    }, 1000)
                }
            })
        }
    },

    mounted(){
        this.onload()
    },
    beforeCreate(){
        this.$store.state.activeNav = null
        this.$store.state.lastStableNav = null
    },
}
</script>