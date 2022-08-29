<template>
    <div class="w-full h-screen border flex items-center justify-center">
        <Transition name="fade" appear>
            <div class="flex flex-row shadow-xl h-10 w-10 rounded-xl bg-white" style="height: 650px; width: 1050px">
                <!-- LEFT SIDE -->
                <div class="relative flex flex-col w-64% login-left-side rounded-tl-xl rounded-bl-xl">
                    <img src="../assets/pattern-randomized.png" class="absolute -top-20 select-none" alt="">
                    <div class="flex pl-10 items-end h-64 z-10">
                        <span class="font-extrabold text-4xl text-sky-400">Yet another POS System</span>
                    </div>
                    <div class="flex flex-col pl-10 mt-5 z-10">
                        <span class="text-2xl font-extrabold text-gray-400">Simple POS.</span>
                        <span class="text-2xl font-extrabold text-gray-400">Better Looking.</span>
                    </div>
                    <!-- FOOTER -->
                    <div class="absolute inset-x-0 bottom-0 pl-10 py-10 z-10 select-none">
                        <img src="../assets/efaestus.svg" height="" alt="" class="select-none">
                    </div>
                </div>

                <!-- RIGHT SIDE -->
                <div class="relative flex-1 login-right-side rounded-tr-xl rounded-br-xl">
                    <!-- LOGIN COMP -->
                    <div class="relative flex px-6 flex-col h-full z-50">
                        <!-- WELCOME -->
                        <div class="flex-0 mt-20">
                            <span class="font-extrabold text-5xl">Welcome</span>
                        </div>

                        <!-- LOGIN -->
                        <form @submit.prevent="login" class="flex flex-col mt-24">
                            <span class="text-2xl font-extrabold">Login <span v-if="incorrectAuth" class="text-red-400 text-base font-medium">Wrong Username or Password</span></span>
                            <input v-model="username" type="text" class="form-control shadow-none mt-4" placeholder="Username">
                            <input v-model="password" type="password" class="form-control shadow-none mt-4" placeholder="Password">

                            <button class="btn-primary mt-4">Login</button>
                        </form>

                        <!-- <div class="flex mt-2">
                            <router-link to="/forgot-password/" class="font-base text-blue-500">Forgot password?</router-link>
                        </div> -->
                    </div>


                    <img class="select-none absolute top-0 right-0 rounded-tr-xl" src="../assets/red-blob.svg" alt="">
                    <img class="select-none absolute bottom-0 left-0" src="../assets/blue-blob.svg" alt="">
                </div>
            </div>
        </Transition>
    </div>
</template>

<style>
    .login-left-side{
        background-repeat: no-repeat;
        background-size:cover;
        background-position: center;
        overflow: hidden;
    }

    .login-right-side{
        background-color: #F3F3F3;
    }
</style>

<script>
    import {mixins} from '@/mixins/mixins.js';

    export default{
        mixins: [mixins],
        name: 'LoginView',
        data(){
            return {
                username: '',
                password: '',
                incorrectAuth: false
            }
        },

        methods: {
            async login(){
                return this.$store.dispatch('userLogin', {
                    username: this.username,
                    password: this.password
                })
                .then(()=>{
                    this.$router.push({name: 'home'})
                })
                .catch(err=>{
                    this.incorrectAuth = true
                    if(err.message.includes('Network') || err.message.includes('network')){
                        this.swalCustom('Network Error', 'Server is reloading... wait for a moment', 'error', true, false, 'Dismiss')
                        this.incorrectAuth = false
                    }
                })
            }
        },

        created(){
            document.title = 'Vue' 
        },
        mounted(){
            if(this.$store.getters.loggedIn){
                console.log(this.$store.state.currentNav)
                if(this.$store.state.currentNav != 'home'){
                    this.$router.push({name: this.$store.state.currentNav})
                } else {
                    this.$router.push({name: 'home'})
                }
            }
        }
    }

</script>