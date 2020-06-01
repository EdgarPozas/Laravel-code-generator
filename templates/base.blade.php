<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="csrf-token" content="{{ csrf_token() }}">

        <title>@yield("title")</title>

    </head>
    <body>

		<div id="app">
#if #use_login#
            <navigation-bar logged={{Auth::check()}}></navigation-bar>
#else
            <navigation-bar></navigation-bar>
#endif
			@yield("body")
        </div>

        <script src="{{asset('js/app.js')}}"></script>
        <script>$.ajaxSetup({headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')}});</script>
    	@yield("scripts")
        
    </body>
</html>
