<template>
    <div class="h-[30rem] w-[48rem] rounded-2xl shadow-lg bg-white py-8 overflow-hidden flex flex-col justify-center items-center relative flex-initial flex-nowrap">
        <div class="self-start mx-8 pt-8 font-black text-3xl">
            <span class="text-white">Sales for this Month</span>
        </div>
        <apexchart width="790" height="400" type="area" :options="chartOptions" :series="series" />
    </div>
</template>

<style scoped>
div{
    background-color: rgb(33, 36, 37);
}
</style>

<script>
import VueApexCharts from "vue3-apexcharts";
import { getAPI } from '@/axios-api'
import {mixins} from '@/mixins/mixins.js'

export default {
    components: {
      apexchart: VueApexCharts,
    },
    mixins: [
        mixins
    ],
    methods: {
    },
    data() {
        return {
            config:{
                headers: {
                    Authorization: `Bearer ${this.$store.state.accessToken}`
                }
            },
            
            chartOptions: {
                colors:['#23fc2b', 'red'],
                chart: {
                    id: "vuechart-example",
                    toolbar: {
                        show: true,
                        offsetX: -654,
                        tools: {
                            download: false,
                            selection: false,
                            pan: false,
                        }
                    },
                },
                tooltip: {
                    x: {
                        format: 'dd MMM yyyy'
                    },
                    y: {
                        formatter: (item)=>{
                            return `₱${this.formatPrice(item)}`
                        },
                        title: 'Size: 20'
                    },
                },
                fill: {
                    type: 'gradient',
                    gradient: {
                        shadeIntensity: 1,
                        opacityFrom: 0.7,
                        opacityTo: 0.0,
                        stops: [0, 100]
                    }
                },
                xaxis: {
                    type:'datetime',
                    labels: {
                        show:true,
                        style:{
                            fontFamily: 'Montserrat',
                            fontWeight: 'bold',
                            colors: 'white'
                        }
                    },
                    axisBorder: {
                        show: false,
                    }
                },
                yaxis: {
                    forceNiceScale: 1,
                    show:1,
                    floating: 1,
                    labels: {
                        style: {
                            fontSize: '14px',
                            fontFamily: 'Montserrat, sans-serif',
                            fontWeight: 'bold',
                            colors: '#757575',
                            cssClass: '-z-50'
                        },

                        offsetX: 760,
                        formatter: (item)=>{
                            return `₱${this.formatPrice(item)}`
                        }
                    }
                },
                grid: {
                    show: 0,
                    borderColor: '#474d50',
                    xaxis: {
                        lines: {
                            show: 0  //or just here to disable only x axis grids
                        }
                    },
                    yaxis: {
                        lines: {
                            show: true  //or just here to disable only x axis grids
                        }
                    }
                },
                stroke: {
                    curve: 'smooth'
                },
                dataLabels: {
                    enabled: false,
                },
                legend: {
                    show: true,
                    labels: {
                        colors: 'white'
                    }
                }
            },
            noData: {
                text: 'Loading...'
            },
            series: [],
        };
    },

    mounted(){
        getAPI.get('/sales-graph/', this.config)
        .then(res=>{
            this.series.push(res.data)
        })
        .catch(err=>{
            console.log(err)
        })
    }
}
</script>