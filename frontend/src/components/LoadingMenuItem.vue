<template>
    <div class="flex flex-col item-card bg-gray-50 shrink-0 grow-0 select-none">
        <!-- IMAGE -->
        <div class="h-4/6 flex items-center justify-center menu-image">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="#7dd3fc" stroke-width="4"></circle>
                <path class="opacity-75" fill="#0ea5e9" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
        </div>
        <!-- BODY -->
        <div class="flex-auto p-2 flex flex-col justify-between animate-pulse">
            <div class="flex flex-col">
                <!-- NAME -->
                <div class="font-semibold text-base text-ellipsis whitespace-nowrap truncate">
                    <div class="grid grid-cols-12">
                        <div class="h-2 bg-gray-200 rounded col-span-9 mt-2"></div>
                    </div>
                </div>
                
                <!-- CODE -->
                <div class="font-semibold text-sm text-gray-500 whitespace-nowrap text-ellipsis truncate">
                    <div class="grid grid-cols-12">
                        <div class="h-2 bg-gray-200 rounded col-span-6 mt-4"></div>
                    </div>
                </div>
            </div>

            <!-- PRICE -->
            <div class="text-sm font-semibold text-gray-500">
                <div class="grid grid-cols-3">
                    <div class="h-2 bg-gray-200 rounded col-span-1 mb-1"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
    .item-card{
        height: 18rem;
        width: 13rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px 4px rgba(0,0,0,.1);
        cursor: pointer;
        overflow: hidden;
    }
</style>