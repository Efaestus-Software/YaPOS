<template>
    <div class="flex flex-col item-card bg-gray-50 shrink-0 grow-0 select-none">
        <!-- IMAGE -->
        <div class="h-4/6 flex-none menu-image">
            <slot name="image">
                <img src="@/assets/basket.png" alt="">
            </slot>
        </div>
        <!-- BODY -->
        <div class="flex-auto p-2 flex flex-col justify-between">
            <div class="flex flex-col">
                <!-- NAME -->
                <div class="font-semibold text-base text-ellipsis whitespace-nowrap truncate">
                    <slot name="name" >Name</slot>
                </div>
                
                <!-- CODE -->
                <div class="font-semibold text-sm text-gray-500 whitespace-nowrap text-ellipsis truncate">
                    <slot name="code" >Code</slot>
                </div>
            </div>

            <!-- PRICE -->
            <div class="text-sm font-semibold text-gray-500">
                <slot name="price">₱100.00</slot>
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
        transition: 100ms ease-out;
        outline: 0px solid #7dd3fc;
        overflow: hidden;
    }

    .item-card:hover{
        outline: 4px solid #7dd3fc;
    }

    .item-card:active{
        transition: 100ms ease-out;
        outline: 2px solid #7dd3fc;
    }

    .menu-image img{
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        object-fit: cover;
        height: 100%;
        width: 100%
    }
</style>