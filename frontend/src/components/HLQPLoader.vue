<template>
<div v-for="(n, index) in 5" class="px-2 py-2 rounded-md mx-3" :class="index % 2 === 0 ? 'lq-list' : ''">
    <div class="grid grid-rows-2 gap-4 animate-pulse">
        <div class="grid grid-cols-12">
            <div :class="index % 2 === 0 ? 'bg-red-400' : 'bg-red-300'" class="h-2 rounded col-span-8"></div>
            <div :class="index % 2 === 0 ? 'bg-red-400' : 'bg-red-300'" class="h-2 rounded col-start-12"></div>
        </div>
        <div class="grid grid-cols-12">
            <div :class="index % 2 === 0 ? 'bg-red-400' : 'bg-red-300'" class="h-2 rounded col-span-4"></div>
            <div :class="index % 2 === 0 ? 'bg-red-400' : 'bg-red-300'" class="h-2 rounded col-span-2 col-start-11"></div>
        </div>
    </div>
</div>
</template>

<style scoped>
.lq-container{
    background-color: #FFC5C5;
}

.lq-text{
    color: #FF4848
}

.lq-list{
    background-color: #FF9494
}

::-webkit-scrollbar-thumb {
  background-color: #FF9494 !important;
  border-radius: 10px;
}

</style>