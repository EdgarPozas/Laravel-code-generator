<template>
	<div>
		<div>
			 <form :action="url_form" :method="method">
				<input type="hidden" name="_token" :value="csrf">
#component_form#
#if #remove#
				<input type="submit" @click="remove" value="Remove">
#endif
#if #update#
				<input type="submit" @click="update" value="Update">
				<input type="submit" @click="cancel" value="Cancel"> 
#endif
			</form>
		</div>
	</div>
</template>

<script>

	export default {
		data(){
			return {
				csrf: document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
				item:this.#items#,
				item_aux:{},
				url_form:"",
				method:""
			}
		},
		mounted(){
			Object.assign(this.item_aux, this.item);
		},
		props:["#items#",#props#],
		methods:{
#if #remove#
			remove(evt){
	#if #http_remove#
				this.url_form="#url_remove#";
				this.method="#method_remove#";
	#else
				evt.preventDefault();
				axios.post("#url_remove#",this.item)
				.then(res => {
					window.location.replace("#url_redirect#");
				});
	#endif
			},
#endif
#if #update#
			update(evt){
	#if #http_update#
				this.url_form="#url_update#";
				this.method="#method_update#";
	#else
				evt.preventDefault();
				axios.post("#url_update#",this.item)
				.then(res => {
					Object.assign(this.item_aux, this.item);
				});
	#endif
			},
			cancel(evt){
				evt.preventDefault();
				Object.assign(this.item, this.item_aux);
			}
#endif
		}
	}
</script>