<template>
    <div>
        <div>
            <form action="/register" method="post">
                <input type="hidden" name="_token" :value="csrf">
{{component_form}} 
                <input type="submit" value="Register">             
            </form>
        </div>
    </div>
</template>

<script>
     export default {
        data(){
            return {
                csrf: document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            }
        }
    }
</script>