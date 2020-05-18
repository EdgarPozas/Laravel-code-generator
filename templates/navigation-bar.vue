<template>
    <div>
        <ul>
            <li v-for="bar_item in bar_items">
                <a :href=bar_item.url>{{bar_item.name}}</a>
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        data(){
            return {
                bar_items:[{{navigation_controllers}}],
            }
        }
    }
</script>
