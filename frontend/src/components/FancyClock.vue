<template>

<div class="flex montserrat font-extrabold gap-4">
    <!-- DATE CONTAINER-->
    <div class="flex">
        <!-- DAY NUM -->
        <div class="flex items-center">
            <span class="text-3xl leading-none">{{date}}</span>
        </div>
        <!-- DATES -->
        <div class="flex leading-none flex-col gap-0 font-black text-xs justify-center">
            <span class="text-slate-400">{{day}}</span>
            <span>{{month}}</span>
        </div>
    </div>

    <!-- CLOCK -->
    <div class="flex items-center text-3xl">
        <span>{{hour}}:{{minute}} <span hidden>{{seconds}}</span> {{meridian}}</span>
    </div>
</div>

</template>



<style>

</style>



<script>

export default{
    data(){
        return{
            date: '',
            month: '',
            day: '',
            hour: '',
            minute: '',
            meridian: '',
            seconds: '',
        }
    },
    methods: {
        liveTime(){
            const months = [
                'JAN',
                'FEB',
                'MAR',
                'APR',
                'MAY',
                'JUN',
                'JUL',
                'AUG',
                'SEP',
                'OCT',
                'NOV',
                'DEC'
            ]
            const days = [
                'SUN',
                'MON',
                'TUE',
                'WED',
                'THU',
                'FRI',
                'SAT'
            ]
            let value = new Date()
            this.month = months[value.getMonth()]
            this.day = days[value.getDay()]
            this.date = value.getDate() < 10 ? '0' + value.getDate() : value.getDate()
            this.hour = (((value.getHours() + 24) % 12 || 12) < 10 ? '0' : '') + (value.getHours() + 24) % 12 || 12;
            this.minute = (value.getMinutes()<10?'0':'') + value.getMinutes()
            this.meridian = value.getHours() >= 12 ? 'PM' : 'AM'
            this.seconds = value.getSeconds()
        },
    },

    mounted(){
        this.liveTime()
        setInterval(()=>{
            this.liveTime()
        }, 1000)
    },
}

</script>