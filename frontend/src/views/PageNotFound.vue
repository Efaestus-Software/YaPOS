<template>
    <Nav/>
    <div class="w-full h-screen flex items-center justify-center flex-col">
        <span class="text-9xl font-extrabold text-sky-400">404</span>
        <span class="font-extrabold text-4xl text-slate-800">Page not found</span>

        <span class="link mt-10" @click="$router.go(-1)"><i class="fa-solid fa-arrow-left mr-2"></i>Go Back</span>
    </div>
</template>

<script>
import Nav from '@/components/Nav.vue'
export default{
    components: {
        Nav
    }
}
</script>