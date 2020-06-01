<template>
	<div>
		<div>
			<form :action="url_form" :method="method">
				<input type="hidden" name="_token" :value="csrf">
#component_form#
#if #add#
				<input type="submit" v-if="index_modify==-1" @click="add" value="Add"> 
#endif 
#if #update#
				<input type="submit" v-if="index_modify!=-1" @click="update" value="Update">
				<input type="submit" v-if="index_modify!=-1" @click="cancel" value="Cancel"> 
#endif

			</form>
		</div>
		<div>
			<ul>
				<li v-for="(it,index) in items">
					{{it}}
					<a :href="#url_select#">Show</a>
					<input type="submit" @click="select(index)" value="Select">
					<input type="submit" @click="remove(index)" value="Remove">
				</li>
			</ul>
		</div>
	</div>
</template>

<script>
	 export default {
		data(){
			return {
				csrf: document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
				items:this.#items#,
				item:#model_json#,
				item_aux:#model_json#,
				item_empty:#model_json#,
				url_form:"",
				method:"",
				index_modify:-1
			}
		},
		props:["#items#",#props#],
		methods:{
#if #add#
			add(evt){
	#if #http_add#
				this.url_form="#url_add#";
				this.method="#method_add#";
	#else
				evt.preventDefault();
				axios.#method_add#("#url_add#",this.item)
				.then(res => {
					this.items.push(res.data.data);
					this.reset();
				});
	#endif
			},
#endif
#if #remove#
			remove(index){
	#if #http_remove#
				this.url_form="#url_remove#";
				this.method="#method_remove#";
	#else
				axios.#method_remove#("#url_remove#",this.items[index])
				.then(res => {
					this.items.splice(index,1);
					this.reset();
				});
			},
	#endif
#endif
#if #update#
			update(evt){
	#if #http_update#
				this.url_form="#url_update#";
				this.method="#method_update#";
	#else
				evt.preventDefault();
				axios.#method_update#("#url_update#",this.item)
				.then(res => {
					this.items[this.index_modify]=res.data.data;
					this.reset();
				});
			},
	#endif
			cancel(evt){
				evt.preventDefault();
				this.items[this.index_modify]=this.item_aux;
				this.reset();
			},
#endif
			select(index){
				this.index_modify=index;
				this.item=this.items[this.index_modify];
				Object.assign(this.item_aux, this.item);
			},
			reset(){
				this.index_modify=-1;
				Object.assign(this.item, this.item_empty);
			}
		}
	}
</script>