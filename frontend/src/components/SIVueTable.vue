<template>
    <div class="flex flex-col w-full">
        <div class="flex items-center justify-between mb-4 px-4">
            <div>
                <slot name="buttons"></slot>
            </div>
            <div class="flex flex-row items-center gap-10">
                <div v-if="enableDate" class="flex flex-row items-center gap-4">
                    <div class="form-group flex flex-row items-center gap-2">
                        <label for="">from</label>
                        <input v-model="dateStart" type="date" class="form-control">
                    </div>
                    <div class="form-group flex flex-row items-center gap-2">
                        <label for="">to</label>
                        <input v-model="dateEnd" type="date" class="form-control">
                    </div>
                </div>
                <div v-if="enableSearch" class="input-group">
                    <div class="input-group-prepend">
                        <span class="input-group-text"><i class="fa-solid fa-magnifying-glass"></i></span>
                    </div>
                    <input v-model="search" type="text" class="input-group-control" placeholder="Search">
                </div>
            </div>
        </div>
        <table class="table">
            <thead>
                <th v-for="h in header" :key="h" @click="sortTable(h)">{{ h }} <i class="fa-solid fa-arrow-down-short-wide ml-1"></i></th>
            </thead>
            <tbody>
                <slot name="tbody">
                    <tr v-if="filteredItems2.length" v-for="(item, index) in filteredItems2" @click="toggle(item.id)" :class="[index % 2 === 0 ? 'bg-gray-100' : 'bg-white', item.void ? 'bg-red-100' : '']" :key="index">
                        <template v-for="(tdItem, tdKey, tdIndex) in item">
                            <td v-if="tdKey != 'id' && tdKey != 'void'" :class="tdIndex == 0 && enableLink ? 'link' : ''">
                                <span v-if="tdIndex == 1">{{formatDate(tdItem)}}</span>
                                <span v-else>{{tdItem}}</span>
                            </td>
                        </template>
                    </tr>

                    <tr class="bg-gray-100" v-else>
                        <td colspan="99" class="text-center" v-if="loading"><div class="flex gap-2 items-center justify-center my-6"><div class="spinner-grow text-yellow-400"></div><div class="spinner-grow text-yellow-400 delay-1"></div><div class="spinner-grow text-yellow-400 delay-2"></div></div></td>
                        <td colspan="99" class="text-center" v-else> No Data</td>
                    </tr>
                </slot>
            </tbody>
        </table>
    </div>
</template>

<script>
import {sortBy} from 'lodash';
import { ref } from 'vue';
import { mixins } from '@/mixins/mixins.js'

export default{
    data(){
        return{
            search: '',
            dateStart: '',
            dateEnd: '',

        }
    },

    mixins: [
        mixins
    ],
    props: [
        'header', //HEADERS FOR THE TABLE ; MUST BE ARRAY OF STRINGS
        'data', //DATA ITEMS FOR THE TABLE ; MUST BE ARRAY OBJECT
        'dataIncluded', //DATA KEY THAT IS INCLUDED IN RENDERING ; MUST BE ARRAY OF STRINGS
        'enableLink', //ENABLE LINK ON FIRST COLUMN ; MUST BE BOOLEAN
        'enableSearch', //ENABLE SEARCH ; MUST BE BOOLEAN
        'enableDate', //ENABLE DATE FILTER ; MUST BE BOOLEAN
        'loading', //ENABLE LOADING ; MUST BE BOOLEAN
    ],

    computed:{
        transformItems(){
            return this.data.map(item => {
                return {
                    code: `Invoice # ${item.code}`,
                    date: item.date,
                    customer: item.customer ? item.customer.name : item.temporaryCustomer ? item.temporaryCustomer : '',
                    createdBy: `${item.createdBy.first_name} ${item.createdBy.last_name}`,
                    amountTotal: "₱" + this.formatPrice(item.total),
                    id: item.id,
                    void: item.void,
                }
            });
        },
        filteredItems(){
            return this.transformItems.filter(item=>{
                // return ((item.data1.toLowerCase().indexOf(this.search.toLowerCase()) > -1) || item.data2.toLowerCase().indexOf(this.search.toLowerCase()) > -1)
                for (const [key, value] of Object.entries(item)) {
                    if (item[key].toString().toLowerCase().indexOf(this.search.toLowerCase()) > -1) {
                        return true
                    }
                }
            })
        },

        filteredItems2(){
            return this.filteredItems.filter(item=>{
                // filter items with daterange
                if (this.dateStart && this.dateEnd) {
                    for(const [key, value] of Object.entries(item)){
                        if (item[key] >= this.dateStart && item[key] <= this.dateEnd) {
                            return true
                        }
                    }
                } else {
                    return true
                }
            })
        }
    },

    methods:{
        toggle(id) {
            this.$emit('toggle', id)
        },

        //create a sort function with lodash
        sortTable(col){

            let sort = ref(false)
            let updatedList = ref([])
            sort.value = true
            updatedList.value = sortBy(this.data, col)
        },

        reverseCapitalize(str){
            return str.charAt(0).toLowerCase() + str.slice(1)
        },

        formatPrice(val){
            val = Number(val).toFixed(2)
            var num = val.replace(/,/gi, "");
            var num1 = num.split('.')
            var num2 = num1[0].split(/(?=(?:\d{3})+$)/).join(",");
            val = (num1[1] === undefined ? num2 : num2 + "." + num1[1])
            return val
        },
    },
}
</script>