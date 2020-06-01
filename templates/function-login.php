	public function #function_name#(#function_parameters#){
		$credentials=$request->only(#credentials#);
		if (Auth::attempt($credentials)) {
#if "#request-type#"=="http"
	#if #view_selected#
			return view("#folder#.#view#");
	#else
			return redirect("/");
	#endif
#else
			return response()->json(["code"=>200]);
#endif
		}
#if "#request-type#"=="http"
		return back();
#else
		return response()->json(["code"=>400]);
#endif
	}
