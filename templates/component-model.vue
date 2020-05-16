<template>
    <div>
    	<div>
{{component_form}}
            <button v-if="index_modify==-1" @click="add()">Insert</button>
            <button v-if="index_modify!=-1" @click="update()">Update</button>
            <button v-if="index_modify!=-1" @click="cancel()">Cancel</button>
    	</div>
    	<ul>
    		<li v-for="(item,index) in items">
                {{item}}
                {{url_item}}
    			<button @click="select(index)">Select</button>
    			<button @click="remove(index)">Delete</button>
    		</li>
    	</ul>
    </div>
</template>

<script>

     export default {
        data(){
            return {
                items:this.{{items}},
                item_actual:{{{component_json}}},
                item_actual_aux:{{{component_json}}},
                index_modify:-1
            }
        },
        props:[{{props}}],
        methods:{
            add(){
                axios.post("{{url_add}}",this.item_actual)
                .then(res => {
                    this.items.push(res.data.item);
                    this.reset();
                });
            },
            remove(index){
                axios.post("{{url_remove}}",this.items[index])
                .then(res => {
                    this.items.splice(index,1);
                    this.reset();
                });
            },
            update(){
                axios.post("{{url_update}}",this.item_actual)
                .then(res => {
                    this.reset();
                });
            },
            cancel(){
                this.items[this.index_modify]=this.item_actual_aux;
                this.reset();
            },
            select(index){
                this.index_modify=index;
                this.item_actual=this.items[index];
                Object.assign(this.item_actual_aux, this.item_actual);
            },
            reset(){
                this.index_modify=-1;
                this.item_actual={{{component_json}}};
            }
        }
    }
</script>