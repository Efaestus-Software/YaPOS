<template>
    <Transition>
        <div class="backdrop" @click.self="closeModal()" v-if="showModal">
            <Transition appear name="slide-fade">
                <div class="modal rounded-xl shadow-xl flex flex-col">
                    <!-- HEADER -->
                    <div class="flex justify-between px-3 py-3 bg-white rounded-t-xl flex flex-between text-xl font-bold gap-5">
                        <span>Add Supplier</span>
                        <span @click="closeModal()"><i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i></span>
                    </div>

                    <!-- BODY -->
                    <form @submit.prevent="submitAddParty">
                        <div class="px-6 py-4 flex flex-col gap-8">
                            <div class="flex flex-row gap-4 items-center">
                                <div class="form-group">
                                    <label for="">Name</label>
                                    <div class="input-group">
                                        <div class="input-group-prepend">
                                            <span class="input-group-text"><i class="fa-solid fa-user"></i></span>
                                        </div>
                                        <input v-model="addParty.name" type="text" class="input-group-control" placeholder="Enter Supplier's Name" required>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label for="">Address</label>
                                    <div class="input-group">
                                        <div class="input-group-prepend">
                                            <span class="input-group-text"><i class="fa-solid fa-location-dot"></i></span>
                                        </div>
                                        <input v-model="addParty.address" type="text" class="input-group-control" placeholder="Enter Supplier's Address" required>
                                    </div>
                                </div>
                            </div>
                            <div class="flex flex-row gap-4 items-center">
                                <div class="form-group">
                                    <label for="">Contact</label>
                                    <div class="input-group">
                                        <div class="input-group-prepend">
                                            <span class="input-group-text"><i class="fa-solid fa-phone"></i></span>
                                        </div>
                                        <input v-model="addParty.contact" type="tel" class="input-group-control" placeholder="Enter Supplier's Contact" required>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label for="">Email</label>
                                    <div class="input-group">
                                        <div class="input-group-prepend">
                                            <span class="input-group-text"><i class="fa-solid fa-at"></i></span>
                                        </div>
                                        <input v-model="addParty.email" type="email" class="input-group-control" placeholder="Enter Supplier's Email" required>
                                    </div>
                                </div>
                            </div>            
                        </div>
                        <button class="modal-submit-button-primary" type="submit">
                            Save
                        </button>
                    </form>
                </div>
                
            </Transition>
        </div>
    </Transition>
</template>

<style>
    .modal{
        margin: 4rem auto;
        display: flex;
        flex-grow: 0;
        flex-shrink: 0;
        background-color: #F0F2F3;
    }

    .backdrop{
        top: 0;
        left: 0;
        position: fixed;
        background: rgba(0,0,0,0.5);
        backdrop-filter: blur(20px);
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        overflow-y: auto;
    }
</style>

<script>
import { mixins } from '@/mixins/mixins.js'
import { getAPI } from '@/axios-api'
import Modal from '@/components/Modal.vue'

export default {

    data() {
        return {
            showModal: false,
            config:{
                headers: {
                    Authorization: `Bearer ${this.$store.state.accessToken}`
                }
            },

            addParty: {
                name: '',
                address: '',
                contact: '',
                email: ''
            }
        }
    },

    components: {
        Modal
    },

    mixins: [
        mixins
    ],
    methods: {
        clearInputs(){
            this.addParty.name = ''
            this.addParty.address = ''
            this.addParty.contact = ''
            this.addParty.email = ''
        },

        closeModal(){
            this.$emit('close')
        },

        success(){
            this.$emit('success')
            this.clearInputs()
        },

        fail(){
            this.$emit('fail')
            this.clearInputs()
        },

        submitAddParty() {
            let message = "Adding Supplier"
            this.$swal({
                    showConfirmButton: false,
                    allowOutsideClick: false,
                    title: `${message}...`,
            })
            setTimeout(()=>{
                getAPI.post('/suppliers/', this.addParty, this.config)
                .then(res => {
                    this.closeModal()
                    this.success()
                })
                .catch(err => {
                    this.closeModal()
                    this.fail()
                })
            }, 1000)
        }
    }
}
</script>