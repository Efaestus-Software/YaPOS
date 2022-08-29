<template>
    <div id="payment-input" class="bg-white rounded-xl shadow-lg">
        <!-- TOTAL -->
        <div class="px-5 py-4 flex items-center justify-between">
            <div>
                <span class="font-semibold mr-4">Total: ₱{{total}}</span>
                <span class="font-semibold text-green-500" v-if="change >= 0">Change: ₱{{formatPrice(change)}}</span>
                <span class="font-semibold text-red-400" v-else>Change: ₱{{formatPrice(change)}}</span>
            </div>
            <span @click="closeModal" class="text-xl"><i class="fa-solid fa-circle-xmark transition cursor-pointer text-gray-400 hover:text-red-400 text-2xl"></i></span>
        </div>

        <!-- INPUT -->
        <input :value="payInput" type="text" class="outline-0 text-right w-full px-5 py-5 text-4xl font-semibold" readonly>

        <!-- BILLS AND NUMBERS -->
        <div id="num-and-bills" class="flex">
            <div id="numbers" class="flex">
                <div id="keypad" class="flex flex-col p-5">
                    <div id="top-keypad" class="flex font-semibold text-5xl">
                        <div @click="addNumber(7)" class="rounded-md shadow-md flex justify-center items-center key">
                            <span>7</span>
                        </div>
                        <div @click="addNumber(8)" class="rounded-md shadow-md mx-6 flex justify-center items-center key">
                            <span>8</span>
                        </div>
                        <div @click="addNumber(9)" class="rounded-md shadow-md flex justify-center items-center key">
                            <span>9</span>
                        </div>
                    </div>

                    <div id="mid-keypad" class="flex py-5 font-semibold text-5xl">
                        <div @click="addNumber(4)" class="rounded-md shadow-md flex justify-center items-center key">
                            <span>4</span>
                        </div>
                        <div @click="addNumber(5)" class="rounded-md shadow-md mx-6 flex justify-center items-center key">
                            <span>5</span>
                        </div>
                        <div @click="addNumber(6)" class="rounded-md shadow-md flex justify-center items-center key">
                            <span>6</span>
                        </div>
                    </div>

                    <div id="bottom-keypad" class="flex font-semibold text-5xl">
                        <div @click="addNumber(1)" class="rounded-md shadow-md flex justify-center items-center key">
                            <span>1</span>
                        </div>
                        <div @click="addNumber(2)" class="rounded-md shadow-md mx-6 flex justify-center items-center key">
                            <span>2</span>
                        </div>
                        <div @click="addNumber(3)" class="rounded-md shadow-md flex justify-center items-center key">
                            <span>3</span>
                        </div>
                    </div>

                    <div id="bottom-keypad" class="flex pt-5 font-semibold text-5xl">
                        <div @click="addNumber(0)" class="rounded-md shadow-md flex flex-auto justify-center items-center key">
                            <span>0</span>
                        </div>
                        <div @click="addNumber('.')" class="rounded-md shadow-md flex ml-6 justify-center items-center flex-none key">
                            <span>.</span>
                        </div>
                    </div>
                    
                </div>
                <div id="delete" class="flex">
                    <div class="flex flex-1 flex-col font-semibold text-5xl py-5">
                        <div class="rounded-md shadow-md flex justify-center items-center key" @click="deleteNum">
                            <span class="text-4xl"><i class="fa-solid fa-delete-left"></i></span>
                        </div>
                        <div @click="AC" class="rounded-md shadow-md mt-5 flex-1 flex justify-center items-center key text-red-500">
                            <span>AC</span>
                        </div>
                    </div>
                </div>
            </div>
            <div id="bills-coins" class="flex flex-col p-5">
                <div id="bills" class="flex flex-col">
                    <div id="bills-top" class="flex">
                        <img @click="addBill(500)" src="../assets/bills/bill-500.svg" class="rounded-md bills shadow-md" alt="" srcset="">
                        <img @click="addBill(1000)" src="../assets/bills/bill-1000.svg" class="rounded-md bills shadow-md ml-5" alt="" srcset="">
                    </div>
                    <div id="bills-mid" class="flex py-5">
                        <img @click="addBill(100)" src="../assets/bills/bill-100.svg" class="rounded-md bills shadow-md" alt="" srcset="">
                        <img @click="addBill(200)" src="../assets/bills/bill-200.svg" class="rounded-md bills shadow-md ml-5" alt="" srcset="">
                    </div>
                    <div id="bills-bottom" class="flex">
                        <img @click="addBill(20)" src="../assets/bills/bill-20.svg" class="rounded-md bills shadow-md" alt="" srcset="">
                        <img @click="addBill(50)" src="../assets/bills/bill-50.svg" class="rounded-md bills shadow-md ml-5" alt="" srcset="">
                    </div>
                </div>

                <div id="coins" class="flex flex-row justify-between pt-5">
                    <div @click="addBill(1)" class="flex items-center justify-center shadow-md rounded-full key ring-8 ring-gray-500 ring-inset">
                        <span class="font-semibold text-2xl text-gray-500">₱1</span>
                    </div>
                    <div @click="addBill(5)" class="flex items-center justify-center shadow-md rounded-full key ring-8 ring-yellow-400 ring-inset">
                        <span class="font-semibold text-2xl text-yellow-800">₱5</span>
                    </div>
                    <div @click="addBill(10)" class="flex items-center justify-center shadow-md rounded-full key ring-8 ring-yellow-900 ring-inset">
                        <span class="font-semibold text-2xl text-yellow-900">₱10</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- CONFIRM BUTTON -->
        <div @click="closeModal" id="confirm-button" class="flex transition items-center justify-center mt-10 bg-green-500 rounded-b-xl text-green-100 hover:bg-green-600 hover:text-green-200">
            <div class="flex">
                <div class="flex items-center justify-center mr-2"><i class="fa-solid fa-money-bill-wave"></i></div>
                <span class="font-semibold text-xl  py-5">Confirm Payment</span>
            </div>
        </div>

    </div>
</template>

<style scoped>
    .key{
        height: 100px;
        width: 100px;
        background-color: white;
        cursor: pointer;
        user-select: none;
        transition: 25ms;
    }
    .key-disabled{
        height: 100px;
        width: 100px;
        user-select: none;
        transition: 25ms;
    }
    .bills{
        transition: 25ms;
        cursor: pointer;
        user-select: none;
        -webkit-user-drag: none;
    }
    .key:hover{
        background-color: rgb(248, 248, 248);
    }

    .bills:hover{
        filter: brightness(90%);
    }

    .key:active{
        background-color: rgb(236, 236, 236);
    }

    .bils:active{
        filter: brightness(75%)
    }

    #payment-input{
        background-color: #F0F2F3;
    }

    #confirm-button{
        cursor: pointer;
    }
</style>

<script>
    import { mixins } from '@/mixins/mixins'
    export default{
        mixins: [
            mixins
        ],
        data(){
            return{
                pay: ''
            }
        },

        props: [
            'payInput',
            'total',
            'change'
        ],

        methods: {
            addNumber(num){
                this.$emit('addNumber', num)
            },

            addBill(num){
                this.$emit('addBill', num)
            },

            deleteNum(){
                this.$emit('deleteNum')
            },

            AC(){
                this.$emit('AC')
            },
            closeModal(){
                this.$emit('close')
            }
        }
    }
</script>