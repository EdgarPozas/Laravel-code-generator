<template>
    <div>
    	<div>
{{component_form}}
            <button @click="remove()">Delete</button>
            <button @click="update()">Update</button>
            <button @click="cancel()">Cancel</button>
    	</div>
    </div>
</template>

<script>

    export default {
        data(){
            return {
                item_actual:this.{{items}},
                item_actual_aux:{}
            }
        },
        mounted(){
            Object.assign(this.item_actual_aux, this.item_actual);
        },
        props:[{{props}}],
        methods:{
            remove(){
                axios.post("{{url_remove}}",this.item_actual)
                .then(res => {
                    window.location.replace("{{url_redirect}}");
                });
            },
            update(){
                axios.post("{{url_update}}",this.item_actual)
                .then(res => {
                    Object.assign(this.item_actual_aux, this.item_actual);
                });
            },
            cancel(){
                Object.assign(this.item_actual, this.item_actual_aux);
            }
        }
    }
</script>