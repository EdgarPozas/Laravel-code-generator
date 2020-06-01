	public function #function_name#(#function_parameters#){
#if #model_selected#
		$#name_lower#=#name_normal#::#find#;
		$#name_lower#->delete();
		
	#if "#request-type#"=="http"
		#if #view_selected#
		return view("#folder#.#view#");
		#else
		return redirect("/");
		#endif
	#else
		return response()->json(["code"=>200]);
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
