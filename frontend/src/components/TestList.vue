<template>
    <div class="flex flex-col">
        <div class="flex">
            <input v-model="message.message" type="text" class="form-control shadow-md rounded-r-none flex-1" placeholder="Enter message">
            <button @click="sendMessage" class="btn-primary rounded-l-none"> > </button>
        </div>

        <div class="flex flex-col mt-5 bg-white rounded-md p-4 shadow-md">
            <span class="font-bold text-xl">List of Messages</span>
            <div v-for="obj in testList" class="flex flex-col bg-white rounded-md my-1 p-3 shadow-sm border border-gray-200">
                <span class="font-bold text-xl">{{obj.message}}</span>
                <span class="text-sm font-semibold text-gray-500">{{obj.user.username}}</span>
            </div>
        </div>
    </div>
</template>

<script>
    import { getAPI } from '../axios-api'
    export default{
        data(){
            return {
                config: {
                    headers: { 
                        Authorization: `Bearer ${this.$store.state.accessToken}` 
                    }
                },
                testList: null,
                message: {
                    message: null,
                },
            }
        },

        methods: {
            onload(){
                getAPI.get('/test-list/', this.config)
                .then(res=>{
                    this.testList = res.data
                    this.message= {
                        message: null,
                    }
                })
                .catch(err=>{
                    console.table(err)
                })
            },

            sendMessage(){
                getAPI.post('/test-list/', this.message, this.config)
                .then(res=>{
                    this.onload()
                })
                .catch(err=>{
                    console.log(err)
                })
            }
        },
        
        mounted(){
            this.onload()
        }
    }
</script>