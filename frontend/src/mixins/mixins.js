import { getAPI } from '@/axios-api'
export const mixins = {
    methods: {
        validate(evt){
            var theEvent = evt || window.event;
        
            // Handle paste
            if (theEvent.type === 'paste') {
                key = event.clipboardData.getData('text/plain');
            } else {
            // Handle key press
                var key = theEvent.keyCode || theEvent.which;
                key = String.fromCharCode(key);
            }
            var regex = /[0-9]|\./;
            if( !regex.test(key) ) {
              theEvent.returnValue = false;
              if(theEvent.preventDefault) theEvent.preventDefault();
            }
        },

        formatPrice(val){
            val = Number(val).toFixed(2)
            var num = val.replace(/,/gi, "");
            var num1 = num.split('.')
            var num2 = num1[0].split(/(?=(?:\d{3})+$)/).join(",");
            val = (num1[1] === undefined ? num2 : num2 + "." + num1[1])
            return val
        },

        formatPriceIntl(val){
            val = Number(val).toFixed(2)
            let internationalNumberFormat = new Intl.NumberFormat('en-US')
            return internationalNumberFormat.format(val)
        },

        formatDateTime(value){
            const months = [
                'Jan',
                'Feb',
                'Mar',
                'Apr',
                'May',
                'Jun',
                'Jul',
                'Aug',
                'Sep',
                'Oct',
                'Nov',
                'Dec'
            ]

            const days = [
                'Sun',
                'Mon',
                'Tue',
                'Wed',
                'Thu',
                'Fri',
                'Sat'
            ]

            value = new Date(value)
            let year = value.getFullYear()
            let month = months[value.getMonth()]
            let date = value.getDate()
            let hour = (value.getHours() + 24) % 12 || 12; 
            let minute = (value.getMinutes()<10?'0':'') + value.getMinutes()
            let day = days[value.getDay()]
            let meridian = value.getHours() >= 12 ? 'pm' : 'am'
            let formatted = `${month}. ${date}, ${year} - ${hour}:${minute} ${meridian}`

            return formatted
        },

        formatDate(value){
            const months = [
                'Jan',
                'Feb',
                'Mar',
                'Apr',
                'May',
                'Jun',
                'Jul',
                'Aug',
                'Sep',
                'Oct',
                'Nov',
                'Dec'
            ]

            const days = [
                'Sun',
                'Mon',
                'Tue',
                'Wed',
                'Thu',
                'Fri',
                'Sat'
            ]

            value = new Date(value)
            let year = value.getFullYear()
            let month = months[value.getMonth()]
            let date = value.getDate()
            
            let formatted = `${month}. ${date}, ${year}`

            return formatted
        },

        toggleModal(id){
            //check if body has a class of modal-open
            if(document.body.classList.contains('modal-open')){
                //remove class of modal-open
                document.body.classList.remove('modal-open')
            } else {
                //add class of modal-open
                document.body.classList.add('modal-open')
            }
            this.$refs[id].showModal = !this.$refs[id].showModal
        },

        toUpperCase(str){
            return str.toUpperCase()
        },

        getBaseURL(){
            return getAPI.defaults.baseURL
        },

        swalWarning(message){
            this.$swal({
                buttonsStyling: false,
                customClass: {
                    confirmButton: 'btn-primary',
                    cancelButton: 'btn btn-danger',
                },
                title: 'Warning',
                text: message,
                icon: 'warning',
                button: 'OK'
            })
        },

        swalError(message){
            this.$swal({
                buttonsStyling: false,
                customClass: {
                    confirmButton: 'btn-primary',
                    cancelButton: 'btn btn-danger',
                },
                title: 'Error',
                text: message,
                icon: 'error',
                button: 'OK'
            })
        },

        swalSuccess(message){
            this.$swal({
                buttonsStyling: false,
                customClass: {
                    confirmButton: 'btn-primary',
                    cancelButton: 'btn btn-danger',
                },
                title: 'Success',
                text: message,
                icon: 'success',
                button: 'OK'
            })
        },

        swalCustom(title, message, icon, showConfirmButton, showCancelButton, confirmButtonText, cancelButtonText){
            this.$swal({
                buttonsStyling: false,
                customClass: {
                    confirmButton: 'btn-primary',
                    cancelButton: 'btn btn-danger',
                },
                title: title,
                text: message,
                icon: icon,
                showConfirmButton: showConfirmButton,
                showCancelButton: showCancelButton,
                confirmButtonText: confirmButtonText,
                cancelButtonText: cancelButtonText
            })
        },

        swalLoading(title='Loading...', text='Please wait...'){
            this.$swal({
                buttonsStyling: false,
                customClass: {
                    confirmButton: 'btn-primary',
                    cancelButton: 'btn btn-danger',
                },
                title: '<div class="flex gap-2 items-center justify-center my-6"><div class="spinner-grow text-yellow-400"></div><div class="spinner-grow text-yellow-400 delay-1"></div><div class="spinner-grow text-yellow-400 delay-2"></div></div>',
                html: `<span class="text-2xl font-extrabold">${title}</span> <br><br> <span>${text}</span>`,
                showConfirmButton: false,
                showCancelButton: false,
                allowOutsideClick: false,
                allowEscapeKey: false,
                allowEnterKey: false,
                onBeforeOpen: ()=>{
                    this.$swal.showLoading()
                }
            })
        }
    }
}