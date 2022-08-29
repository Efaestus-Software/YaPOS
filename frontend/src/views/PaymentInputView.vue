<template>
    <Nav/>
    <Transition name="fade" appear>
        <div class="w-full flex">
            <div class="xl:container xl:px-0 sm:px-4 flex flex-col mx-auto">
                <div class="flex justify-center">
                    <button class="btn-primary" @click="toggleModal('modal1')">Show Modal</button>
                    <Modal ref="modal1" @close="toggleModal('modal1')">
                        <template v-slot:body>
                            <PaymentInput @close="toggleModal('modal1')" :payInput="formatPrice(payInput)" :subTotal="formatPrice(subTotal)" @addNumber="addNumber" @addBill="addBill" @deleteNum="deleteNum" @AC='AC'/>
                        </template>
                    </Modal>
                </div>
                <div class="flex flex-1 items-center justify-center">

                </div>
            </div>
        </div>
    </Transition>
</template>

<script>
    import PaymentInput from '@/components/PaymentInput.vue'
    import Nav from '@/components/Nav.vue'
    import Modal from '@/components/Modal.vue'

    export default{
        components:{
            PaymentInput,
            Nav,
            Modal
        },

        data(){
            return{
                payInput: '',
                subTotal: 488
            }
        },

        methods: {
            checkIfTwoDecimalPlaces(){
                // return false if over two decimal places
                // return true if less than two decimal places
                if(this.payInput.split('.').length > 1){
                    if(this.payInput.split('.')[1].length > 1){
                        return false
                    }
                }
                return true
            },

            assertSingleDecimalPoint(){
                // return true if there is a single decimal point in the number
                // return false if there is none
                if(this.payInput.split('.').length > 1){
                    return true
                }
                return false
            },

            addNumber(num){
                if (!this.checkIfTwoDecimalPlaces()){
                    return
                }
                if (num == '.' && this.assertSingleDecimalPoint()){
                    return
                }
                this.payInput = String(this.payInput.concat(num))
            },

            addBill(num){
                this.payInput = String(Number(this.payInput) + Number(num))
            },

            deleteNum(){
                this.payInput = String(this.payInput.slice(0, -1))
            },

            // ALL CLEAR
            AC(){
                this.payInput = ''
            },

            formatPrice(num){
                var formatter = new Intl.NumberFormat('en-US', {
                    style: 'currency',
                    currency: 'PHP'
                })

                return formatter.format(num)
            },

            toggleModal(id){
                this.$refs[id].showModal = !this.$refs[id].showModal
            },
        }
    }
</script>