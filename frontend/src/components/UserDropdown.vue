<template>
    <div id="bruh" ref="bruh" class="flex flex-col outline-2 outline outline-gray-300 rounded-xl border" v-if="showDropdown">
        <!-- USER DETAILS -->
        <div class="flex flex-row bg-gray-100 py-4 px-12 items-center justify-center rounded-t-lg font-bold gap-3">
            <!-- PICTURE -->
            <!-- <div class="outline outline-4 outline-gray-300 h-12 w-12 rounded-full">
                <img src="@/assets/download.jpeg" class="rounded-full h-12 w-12" alt="" style="object-fit:cover">
            </div> -->
            <div class="flex flex-col">
                <span>{{$store.state.myDetails.first_name}} {{$store.state.myDetails.last_name}}</span>
                <span class="text-gray-400 font-bold text-sm">{{$store.state.myDetails.username}}</span>
            </div>
        </div>

        <!-- BUTTONS -->
        <div class="flex flex-row p-3 gap-2 items-center justify-center">
            <router-link title="Settings" to="/user-settings/" class="hover:bg-gray-200 active:bg-gray-300 text-left text-slate-600 bg-gray-100 p-3 font-semibold rounded-md outline outline-1 outline-gray-300 h-10 w-10 flex items-center"><i class="fa-solid fa-gear mr-2"></i></router-link>
            <a title="User Guide" :href="getBaseURL() + '/static/files/YaPOS%20User%20Guide.pdf'" class="hover:bg-gray-200 active:bg-gray-300 text-left text-slate-600 bg-gray-100 p-3 font-semibold rounded-md outline outline-1 outline-gray-300 h-10 w-10 flex items-center"><i class="fa-solid fa-book mr-2"></i></a>
            <router-link title="Logout" to="/logout/" class="hover:bg-gray-200 active:bg-gray-300 text-left text-slate-600 bg-gray-100 p-3 font-semibold rounded-md outline outline-1 outline-gray-300 h-10 w-10 flex items-center"><i class="fa-solid fa-right-from-bracket mr-2"></i></router-link>
        </div>
    </div>
</template>

<style>
#bruh{
    box-shadow: 0 2px 30px 0px rgba(0, 0, 0, 0.2);
}
</style>

<script>
import { mixins } from '@/mixins/mixins.js'
    export default{
        mixins: [
            mixins
        ],

        data(){
            return{
                showDropdown: false,
            }
        },

        methods: {
            close() {
                this.showDropdown = !this.showDropdown
            },
        },

        mounted(){
            document.addEventListener('mouseup', event => {
                if (event.target.id == 'toggler') {
                    return
                }

                try{
                    if (!this.$refs.bruh.contains(event.target)) {
                        this.close()
                    }
                }

                catch(err){}
            })
        }
    }
</script>