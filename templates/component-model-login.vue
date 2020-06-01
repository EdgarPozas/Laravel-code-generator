<template>
	<div>
		<div>
			<form :action="url_form" :method="method">
				<input type="hidden" name="_token" :value="csrf">
#component_form#
				<input type="submit" @click="login" value="Login"> 
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
			login(evt){
#if #http_login#
				this.url_form="#url_login#";
				this.method="#method_login#";
#else
				evt.preventDefault();
				axios.#method_login#("#url_login#",this.item)
				.then(res => {
					window.location.replace("/");
				});
#endif
			},
		}
	}
</script>