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
                    BUSINESS SETTINGS
                </div>
                <div class="px-6 py-4 flex flex-col">
                    <!-- <div class="outline outline-2 outline-dashed rounded-md outline-gray-400 flex items-center justify-center text-gray-400 h-36 font-bold cursor-pointer hover:outline-gray-600 hover:text-gray-600">
                        + Add Business Logo
                    </div> -->

                    <span class="font-bold mb-6">
                        Business Information <span class="link font-medium ml-2" @click="toggleModalInfo">Edit </span>
                    </span>

                    <!-- CONTENT -->
                    <div class="grid grid-cols-2 gap-y-12 gap-x-6">
                        <div class="flex flex-col">
                            <label for="" class="text-gray-400 font-bold m-0">Business Name</label>
                            <span v-if="profile.name" class="font-extrabold text-2xl m-0">{{profile.name}}</span>
                            <span v-else class="font-extrabold text-2xl m-0">-</span>
                        </div>
                        <div class="flex flex-col">
                            <label for="" class="text-gray-400 font-bold m-0">Contact / Tel.</label>
                            <span v-if="profile.contact" class="font-extrabold text-2xl m-0">{{profile.contact}}</span>
                            <span v-else class="font-extrabold text-2xl m-0">-</span>
                        </div>
                        <div class="flex flex-col">
                            <label for="" class="text-gray-400 font-bold m-0">Email</label>
                            <span v-if="profile.email" class="font-extrabold text-2xl m-0">{{profile.email}}</span>
                            <span v-else class="font-extrabold text-2xl m-0">-</span>
                        </div>
                        <div class="flex flex-col">
                            <label for="" class="text-gray-400 font-bold m-0">Website</label>
                            <span v-if="profile.website" class="font-extrabold text-2xl m-0">{{profile.website}}</span>
                            <span v-else class="font-extrabold text-2xl m-0">-</span>
                        </div>
                        <div class="flex flex-col col-span-2">
                            <label for="" class="text-gray-400 font-bold m-0">Address</label>
                            <span v-if="profile.address" class="font-extrabold text-lg m-0">{{profile.address}}</span>
                            <span v-else class="font-extrabold text-2xl m-0">-</span>
                        </div>
                        <div class="flex flex-col col-span-2">
                            <label for="" class="text-gray-400 font-bold m-0">TIN</label>
                            <span v-if="profile.tin" class="font-extrabold text-lg m-0">{{profile.tin}}</span>
                            <span v-else class="font-extrabold text-2xl m-0">-</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Transition>




    <!-- MODAL 1 -->
    <Modal ref="editInfo" @close="toggleModal('editInfo')">
        <template v-slot:header>
            <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold">
                <span>Edit Business Info</span>
                <span @click="toggleModal('editInfo')"><i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i></span>
            </div>
        </template>

        <template v-slot:body>
            <form @submit.prevent="submitInfo()">
                <div class="flex flex-row px-6 py-4 gap-4 w-[40rem]">
                    <div class="grid grid-cols-2 gap-6">
                        
                        <div class="form-group w-full">
                            <label for="">Business Name <span class="text-xs text-gray-400">Required</span></label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">
                                        <i class="fa-solid fa-building"></i>
                                    </span>
                                </div>
                                <input v-model="editProfile.name" type="text" class="input-group-control" placeholder="Enter Business Name" required>
                            </div>
                        </div>
                        
                        <div class="form-group w-full">
                            <label for="">Contact / Tel.</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">
                                        <i class="fa-solid fa-phone"></i>
                                    </span>
                                </div>
                                <input v-model="editProfile.contact" type="text" class="input-group-control" placeholder="Enter Contact / Tel.">
                            </div>
                        </div>
                        
                        <div class="form-group w-full">
                            <label for="">Email</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">
                                        <i class="fa-solid fa-envelope"></i>
                                    </span>
                                </div>
                                <input v-model="editProfile.email" type="text" class="input-group-control" placeholder="Enter Email">
                            </div>
                        </div>
                        
                        <div class="form-group w-full">
                            <label for="">Website</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">
                                        <i class="fa-solid fa-globe"></i>
                                    </span>
                                </div>
                                <input v-model="editProfile.website" type="text" class="input-group-control" placeholder="Enter Website">
                            </div>
                        </div>

                        <div class="form-group w-full col-span-2">
                            <label for="">Address</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">
                                        <i class="fa-solid fa-map-marker"></i>
                                    </span>
                                </div>
                                <input v-model="editProfile.address" type="text" class="input-group-control" placeholder="Enter Address">
                            </div>
                        </div>

                        <div class="form-group w-full col-span-2">
                            <label for="">TIN</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">
                                        <i class="fa-solid fa-t"></i>
                                    </span>
                                </div>
                                <input v-model="editProfile.tin" type="text" class="input-group-control" placeholder="Enter TIN">
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

            profile: {
                name: '',
                email: '',
                contact: '',
                website: '',
                address: '',
                tin: ''
            },

            editProfile: {
                name: '',
                email: '',
                contact: '',
                website: '',
                address: '',
                tin: ''
            }
        }
    },
    beforeCreate(){
        this.$store.state.activeNav = null
        this.$store.state.lastStableNav = null
    },

    methods: {
        onload(){
            getAPI.get('/business-profile/', this.config)
            .then(res=>{
                this.profile = res.data
            });
        },
        toggleModalInfo(){
            this.editProfile = {...this.profile}
            this.toggleModal('editInfo')
        },

        submitInfo(){
            this.swalLoading('Updating...')
            setTimeout(() => {
            getAPI.post('/business-profile/', this.editProfile, this.config)
                .then(res => {
                    this.swalSuccess('Successfully updated')
                    this.onload()
                    this.toggleModal('editInfo')
                })
                .catch(err => {
                    this.swalError(err.message)
                })
            }, 1000);
        }
    },

    mounted(){
        getAPI.get('/business-profile/', this.config)
        .then(res=>{
            this.profile = res.data
        })
    }
}
</script>