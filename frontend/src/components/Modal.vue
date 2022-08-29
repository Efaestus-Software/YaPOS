<template>
    <Transition>
        <div class="backdrop z-50" @click.self="closeModal()" v-if="showModal">
            <Transition appear name="slide-fade">
                <div class="modal rounded-xl shadow-xl flex flex-col">
                    <slot name="header"></slot>
                    <slot name="body"></slot>
                    <slot name="footer"></slot>
                    <slot></slot>
                </div>
            </Transition>
        </div>
    </Transition>
</template>

<script>
    export default{
        props: ['header', 'id'],
        data(){
            return{
                showModal: false,
            }
        },

        methods: {
            closeModal(){
                this.$emit('close')
            }
        }
    }
</script>

<style>
body.modal-open{
    overflow: hidden;
}

.modal{
    margin: 10rem auto;
    display: flex;
    flex-grow: 0;
    flex-shrink: 0;
    background-color: #F0F2F3;
}

.backdrop{
    top: 0;
    left: 0;
    position: fixed;
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(20px);
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow-y: auto !important;
}
</style>