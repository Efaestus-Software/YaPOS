<template>
    <div class="z-20 flex items-center justify-between w-100 sticky top-0 shadow-xl mb-4 nav shrink-0">
        <div class="w-[10%] pl-4 h-full flex items-center">
            <router-link to="/" class="font-bold text-sky-500 ">YaPOS</router-link>
        </div>
        <div class="">
            <router-link class="nav-link" to="/" id="home">Home</router-link>
            <router-link class="nav-link" to="/sales" id="sales">Sales</router-link>
            <router-link class="nav-link" to="/inventory" id="inventory">Inventory</router-link>
            <router-link class="nav-link" to="/receive" id="receive">Receive</router-link>
            <router-link class="nav-link" to="/adjustments" id="adjustments">Adjustments</router-link>
            <router-link class="nav-link" to="/suppliers" id="suppliers">Suppliers</router-link>
            <router-link class="nav-link" to="/customers" id="customers">Customers</router-link>
            <router-link class="nav-link" to="/si-list" id="si-list">Reports</router-link>

        </div>
        <div class="w-[10%] pr-4 h-full flex items-center justify-end relative">
            <div class="cursor-pointer text-slate-500 select-none text-2xl"><i id="toggler" @click="toggleUserDropdown('userDropdown')" class="fa-solid fa-circle-user"></i></div>
        </div>
    </div>
    <Transition name="slide-fade-2">
        <UserDropdown ref="userDropdown" class="fixed right-5 top-16 z-10 b-blur" />
    </Transition>
</template>

<script>
    import UserDropdown from '@/components/UserDropdown.vue'

    export default{
        components:{
            UserDropdown,
        },
        computed: {
            getCurrentRoute(){
                return this.$route.name
            }
        },
        methods: {
            onload(){
                try{
                    let x = document.getElementById(this.getCurrentRoute)
                    x.classList.add('text-[#1EBAEB]')
                    this.$store.commit('changeLastStableNav', this.getCurrentRoute)
                }
                catch(err){
                    try{
                        let x = document.getElementById(this.$store.state.lastStableNav)
                        x.classList.add('text-[#1EBAEB]')
                    } catch(err){
                        console.log('error from nav')
                    }
                }
            },

            toggleUserDropdown(id){
                this.$refs.userDropdown.close()
            }

            // changeNav(id){
            //     this.$store.commit('changeCurrentNav', id)
            // }
        },

        mounted(){
            this.onload()
        }
    }
</script>

<style scoped>
    a.nav-link{
        margin: 0px 1.5rem;
        font-weight: 600;
        font-size: 14px;
        transition: 100ms;
    }

    a.nav-link:hover{
        transition: 100ms;
    }

    .nav{
        backdrop-filter:blur(25px);
        background-color: rgba(255,255,255,0.75);
        height: 52px;
    }

    .b-blur{
        backdrop-filter:blur(25px);
        background-color: rgba(255,255,255,0.75);
    }
</style>