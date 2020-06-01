<template>
	<div>
		<ul>
			<li v-for="bar_item in bar_items">
				<a :href=bar_item.url>{{bar_item.name}}</a>
			</li>
#if #use_login#
			<div v-if="logged">
				<li>
					<a href="/logout">Exit</a>
				</li>
			</div>
			<div>
				<li>
					<a href="/login">Login</a>
				</li>
				<li>
					<a href="/register">Register</a>
				</li>
			</div>
#endif
		</ul>
	</div>
</template>

<script>
	export default {
		data(){
			return {
				bar_items:[#navigation_controllers#]
			}
		},
#if #use_login#
		props:["logged"]
#endif
	}
</script>
