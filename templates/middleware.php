<?php

namespace App\Http\Middleware;

use Auth;
use Closure;

class #name#
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
#if #type#=="login"
        if(!Auth::check())
            return redirect("/");
        return $next($request);
#else
        return $next($request); 
#endif
    }
}
