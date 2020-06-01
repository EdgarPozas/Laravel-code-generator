	public function #function_name#(#function_parameters#){
#if #model_selected#
		$#name_lower#s=#name_normal#::all();
		
	#if "#request-type#"=="http"
		#if #view_selected#
		return view("#folder#.#view#",["data"=>$#name_lower#s]);
		#else
		return redirect("/");
		#endif
	#else
		return response()->json(["code"=>200,"data"=>$#name_lower#s]);
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
