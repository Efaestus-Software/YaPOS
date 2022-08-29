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
                <div class="font-black text-3xl px-6 py-4">
                    USER SETTINGS
                </div>
                <div class="px-6 py-4 flex flex-col">
                    <!-- TITLE -->
                    <span class="font-bold mb-6">
                        Personal Information <span class="link font-medium ml-2" @click="toggleModalInfo">Edit Name</span> <span class="link font-medium ml-2" @click="toggleChangeUsername">Change Username</span>
                    </span>

                    <!-- CONTENT -->
                    <div class="flex flex-row items-center gap-6">
                        <!-- IMG -->
                        <!-- <img src="@/assets/user.png" alt="" class="h-[8rem] w-[8rem] border border-2 rounded-full" style="object-fit:cover"> -->
                        <div class="flex flex-col gap-4">
                            <div class="flex flex-col">
                                <label for="" class="text-gray-400 font-bold m-0">Name</label>
                                <span class="font-extrabold text-2xl m-0">{{me.first_name}} {{me.last_name}}</span>
                            </div>
                            <div class="flex flex-col">
                                <label for="" class="text-gray-400 font-bold m-0">Username</label>
                                <span class="font-extrabold text-2xl m-0">{{me.username}}</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="px-6 py-4 flex flex-col">
                    <!-- TITLE -->
                    <span class="font-bold mb-6">
                        Email & Password <span class="link font-medium ml-2" @click="toggleModalEmail">Change Email</span> <span class="link font-medium ml-2" @click="toggleModal('editPassword')">Change Password</span>
                    </span>

                    <!-- CONTENT -->
                    <div class="flex flex-col">
                        <label for="" class="text-gray-400 font-bold m-0">Email</label>
                        <span class="font-extrabold text-lg m-0" v-if="me.email">{{me.email}}</span>
                        <span class="font-extrabold text-lg m-0" v-else>No email</span>
                    </div>
                </div>
            </div>
        </div>
    </Transition>

    <!-- MODAL 1 -->
    <Modal ref="editInfo" @close="toggleModal('editInfo')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Edit Personal Info</span>
                <span @click="toggleModal('editInfo')"><i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i></span>
            </div>
        </template>

        <template v-slot:body>
            <form @submit.prevent="submitInfo()">
                <div class="flex flex-row px-6 py-4 gap-4 w-[28rem]">
                    <!-- <div class="img flex flex-col items-center justify-center">
                        <input accept="image/*" type="file" id="imageInputEdit" @change="onFileChangeEdit($event)" hidden>
                        <div @click="chooseFileEdit('imageInputEdit')" class="flex h-[8rem] w-[8rem] border rounded-full over select-none outline-2 outline-dashed outline-gray-400 items-center justify-center relative text-gray-400 font-bold cursor-pointer hover:outline-gray-600 hover:text-gray-600">
                            + Add Photo
                        </div>
                    </div> -->

                    <div class="flex flex-1 flex-col gap-4 justify-center">
                        <!-- FIRST NAME -->
                        <div class="form-group w-full">
                            <input v-model='editInfo.first_name' type="text" class="form-control" placeholder="Enter your First Name" required>
                        </div>
                        <!-- LAST NAME -->
                        <div class="form-group w-full">
                            <input v-model="editInfo.last_name" type="text" class="form-control" placeholder="Enter your Last Name" required>
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
    <Modal ref="editEmail" @close="toggleModal('editEmail')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Edit Email</span>
                <span @click="toggleModal('editEmail')"><i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i></span>
            </div>
        </template>

        <template v-slot:body>
            <form @submit.prevent="submitEmail">
                <div class="flex flex-row px-6 py-4 gap-4 w-[28rem]">
                    <div class="form-group w-full">
                        <label for="">Email</label>
                        <div class="input-group">
                            <div class="input-group-prepend">
                                <span class="input-group-text">
                                    <i class="fa-solid fa-at"></i>
                                </span>
                            </div>
                            <input v-model="editEmail.email" type="email" class="input-group-control" placeholder="Enter your Email" required>
                        </div>
                    </div>
                </div>
                <button class="modal-submit-button-primary" type="submit">
                    Save
                </button>
            </form>
        </template>
    </Modal>

    <!-- MODAL 3 -->
    <Modal ref="editPassword" @close="toggleModal('editPassword')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Edit Password</span>
                <span @click="toggleModal('editPassword')"><i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i></span>
            </div>
        </template>

        <template v-slot:body>
            <form @submit.prevent="submitPassword">
                <div class="flex flex-col px-6 py-4 gap-4 w-[28rem]">
                    <div class="form-group w-full">
                        <label for="">Current Password</label>
                        <input required v-model="editPassword.current_password" type="password" class="form-control" placeholder="Enter your current password">
                    </div>

                    <div class="form-group w-full mt-4">
                        <label for="">New Password</label>
                        <input required v-model="editPassword.new_password" type="password" class="form-control" placeholder="Enter your new password">
                    </div>
                    <div class="form-group w-full">
                        <label for="">Verify Password</label>
                        <input required v-model="editPassword.verify_password" :class="[editPassword.new_password != editPassword.verify_password ? 'outline outline-4 outline-red-300' : 'outline outline-4 outline-green-300']" type="password" class="transition form-control" placeholder="Verify password">
                    </div>
                </div>
                <button class="modal-submit-button-primary" type="submit">
                    Save
                </button>
            </form>
        </template>
    </Modal>

    <!-- MODAL 4 -->
    <Modal ref="changeUsername" @close="toggleModal('changeUsername')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Edit Change Username</span>
                <span @click="toggleModal('changeUsername')"><i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i></span>
            </div>
        </template>

        <template v-slot:body>
            <form @submit.prevent="submitChangeUsername()">
                <div class="flex flex-row px-6 py-4 gap-4 w-[28rem]">
                    <!-- <div class="img flex flex-col items-center justify-center">
                        <input accept="image/*" type="file" id="imageInputEdit" @change="onFileChangeEdit($event)" hidden>
                        <div @click="chooseFileEdit('imageInputEdit')" class="flex h-[8rem] w-[8rem] border rounded-full over select-none outline-2 outline-dashed outline-gray-400 items-center justify-center relative text-gray-400 font-bold cursor-pointer hover:outline-gray-600 hover:text-gray-600">
                            + Add Photo
                        </div>
                    </div> -->

                    <div class="flex flex-1 flex-col gap-4 justify-center">
                        <!-- FIRST NAME -->
                        <div class="form-group w-full">
                            <input v-model='changeUsername.username' type="text" class="form-control" placeholder="Enter Username" required>
                        </div>
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

            me: {
                first_name: '',
                last_name: '',
                username: '',
                email: '',
            },

            editInfo: {
                first_name: '',
                last_name: ''
            },

            editEmail: {
                email: ''
            },

            changeUsername: {
                username: ''
            },

            editPassword: {
                current_password: '',
                new_password: '',
                verify_password: ''
            }
        }
    },

    methods: {
        chooseFileEdit(id){
            document.getElementById(id).click()
        },

        toggleModalInfo(){
            this.editInfo.first_name = this.me.first_name
            this.editInfo.last_name = this.me.last_name
            this.toggleModal('editInfo')
        },

        toggleModalEmail(){
            this.editEmail.email = this.me.email
            this.toggleModal('editEmail')
        },

        toggleChangeUsername(){
            this.changeUsername.username = this.me.username
            this.toggleModal('changeUsername')
        },

        submitInfo(){
            this.swalLoading('Updating...')
            setTimeout(() => {
                getAPI.post('/update-my-name/', this.editInfo, this.config)
                .then(res=>{
                    this.resetInfo()
                    this.toggleModal('editInfo')
                    this.swalSuccess('Successfully updated')
                    this.onload()
                })
                .catch(err=>{
                    this.swalError(err.message)
                })
            }, 1000);
        },

        resetChangeUsername(){
            this.changeUsername.username = ''
        },

        submitChangeUsername(){
            this.swalLoading('Updating...')
            setTimeout(() => {
                getAPI.post('/update-my-username/', this.changeUsername, this.config)
                .then(res=>{
                    this.resetChangeUsername()
                    this.toggleModal('changeUsername')
                    this.swalSuccess('Successfully updated')
                    this.onload()
                })
                .catch(err=>{
                    this.swalError(err.message)
                })
            }, 1000);
        },

        submitEmail(){
            this.swalLoading('Updating...')
            setTimeout(() => {
                getAPI.post('/update-my-email/', this.editEmail, this.config)
                .then(res=>{
                    this.resetEmail()
                    this.toggleModal('editEmail')
                    this.swalSuccess('Successfully updated')
                    this.onload()
                })
                .catch(err=>{
                    this.swalError(err.message)
                })
            }, 1000);
        },

        submitPassword(){
            this.swalLoading('Updating...')
            setTimeout(() => {
                getAPI.post('/update-my-password/', this.editPassword, this.config)
                .then(res=>{
                    if(res.data == 0){
                        this.resetPassword()
                        this.toggleModal('editPassword')
                        this.swalSuccess('Successfully updated')
                        this.onload()
                    }
                    else if(res.data == 1){
                        this.swalError('Old password is incorrect')
                    }
                })
                .catch(err=>{
                    this.swalError(err.message)
                })
            }, 1000);
        },

        resetInfo(){
            this.editInfo.first_name = ''
            this.editInfo.last_name = ''
        },

        resetEmail(){
            this.editEmail.email = ''
        },

        resetPassword(){
            this.editPassword.current_password = ''
            this.editPassword.new_password = ''
            this.editPassword.verify_password = ''
        },

        onload(){
            getAPI.get('/me/', this.config)
            .then(res=>{
                this.me = res.data
            })
            .catch(err=>{
                console.log(err)
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