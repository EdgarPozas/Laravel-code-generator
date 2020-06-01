	public function #function_name#(#function_parameters#){
		Auth::logout();
		
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
