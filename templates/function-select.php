	public function #function_name#(#function_parameters#){
#if #model_selected#
		$#name_lower#=#name_normal#::#find#->first();
		
	#if "#request-type#"=="http"
		#if #view_selected#
		return view("#folder#.#view#",["data"=>$#name_lower#]);
		#else
		return redirect("/");
		#endif
	#else
		return response()->json(["code"=>200,"data"=>$#name_lower#]);
	#endif
#else
	#if "#request-type#"=="http"
		#if #view_selected#
		return view("#folder#.#view#");
		#else
		return redirect("/");
		#endif
	#else
		return response()->json(["code"=>200]);
	#endif
#endif
	}
