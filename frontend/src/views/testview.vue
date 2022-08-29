<template>
    <Nav />
    <SubNav>
        <template v-slot:body>
            <router-link to="/inventory" id="sub-inventory">Products</router-link>
            <router-link to="/test" id="sub-test">List</router-link>
        </template>
    </SubNav>
    <div class="container mx-auto">
        <div class="flex flex-col justify-center">
            <form @submit.prevent="addInventory">
                <div class="form-group">
                    <label for="">Inv Name</label>
                    <!-- input with v-model myInventory-->
                    <input v-model="myInventory.name" type="text" class="form-control" id="name"
                        placeholder="Enter name">
                </div>
                <div class="form-group">
                    <!-- Inventory code -->
                    <label for="">Inv Code</label>
                    <!-- input with v-model myInventory-->
                    <input v-model="myInventory.code" type="text" class="form-control" id="code"
                        placeholder="Enter code">
                </div>
                <!-- form group for qty -->
                <div class="form-group">
                    <label for="">Qty</label>
                    <!-- input with v-model myInventory-->
                    <input v-model="myInventory.qty" type="number" class="form-control" id="qty"
                        placeholder="Enter qty">
                </div>
                <!-- form gorup for selling price -->
                <div class="form-group">
                    <label for="">Selling Price</label>
                    <!-- input with v-model myInventory-->
                    <input v-model="myInventory.sellingPrice" type="number" step="0.01" class="form-control"
                        id="selling_price" placeholder="Enter selling price">
                </div>
                <!-- form group for unit cost -->
                <div class="form-group">
                    <label for="">Unit Cost</label>
                    <!-- input with v-model myInventory-->
                    <input v-model="myInventory.unitCost" type="number" step="0.01" class="form-control" id="unit_cost"
                        placeholder="Enter unit cost">
                </div>
                <!-- button for submit -->
                <button class="btn-primary mt-4" type="submit">Submit</button>
            </form>
        </div>
    </div>
</template>

<script>
    import Nav from '@/components/Nav.vue'
    import SubNav from '@/components/SubNav.vue'
    import { getAPI } from '../axios-api'
    export default{
        components: {
            Nav,
            SubNav
        },

        data(){
            return{
                config: {
                    headers: {
                        Authorization: `Bearer ${this.$store.state.accessToken}`
                    }
                },
                data: [],

                myInventory: {
                    name: null,
                    code: null,
                    qty: null,
                    sellingPrice: null,
                    unitCost: null,
                    image: null,
                    category: null,
                }
            }
        },

        methods:{
            onload(){
                getAPI.get('/inventory/', this.config)
                .then(res=>{
                    this.data = res.data
                })
            },
            // add method to clear myInventory
            clearMyInventory(){
                this.myInventory = {
                    name: null,
                    code: null,
                    qty: null,
                    sellingPrice: null,
                    unitCost: null,
                    image: null,
                    category: null,
                }
            },
            // a method to submit this.myInventory
            addInventory(){
                getAPI.post('/inventory/', this.myInventory, this.config)
                .then(res=>{
                    this.$swal({
                        buttonsStyling: false,
                        customClass: {
                            confirmButton: 'btn-primary',
                            cancelButton: 'btn btn-danger',
                        },
                        title: 'Success',
                        text: 'Inventory added',
                        icon: 'success',
                        button: 'OK'
                    })
                    this.clearMyInventory()
                    this.onload()
                })
                .catch(err=>{
                    this.$swal({
                        buttonsStyling: false,
                        customClass: {
                            confirmButton: 'btn-primary',
                            cancelButton: 'btn btn-danger',
                        },
                        title: 'Error',
                        text: 'Someting went wrong',
                        icon: 'error',
                        button: 'OK'
                    })
                    console.log(err)
                })
            }
        },

        mounted(){
            this.onload()
        }
    }    
</script>