<template>
	<div>
		<div>
			<form :action="url_form" :method="method">
				<input type="hidden" name="_token" :value="csrf">
#component_form#
				<input type="submit" @click="add" value="Add"> 
			</form>
		</div>
	</div>
</template>

<script>
	 export default {
		data(){
			return {
				csrf: document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
				item:#model_json#,
				url_form:"",
				method:""
			}
		},
		methods:{
			add(evt){
#if #http_add#
				this.url_form="#url_add#";
				this.method="#method_add#";
#else
				evt.preventDefault();
				axios.#method_add#("#url_add#",this.item)
				.then(res => {
					window.location.replace("/");
				});
#endif
			},
		}
	}
</script>