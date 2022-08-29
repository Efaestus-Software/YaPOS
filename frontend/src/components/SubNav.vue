<template>

    <div class="sub-nav flex flex-row font-semibold gap-6 items-center justify-center self-center mb-3 text-sm">
        <slot name="body"></slot>
    </div>

</template>

<script>
    export default{
        computed:{
            getCurrentRoute(){
                return this.$route.name
            }
        },

        methods:{
            onload(){
                let x = document.getElementById(`sub-${this.getCurrentRoute}`)
                x.classList.add('text-[#1EBAEB]')
            }
        },
        mounted(){
            this.onload()
        }
    }
</script>