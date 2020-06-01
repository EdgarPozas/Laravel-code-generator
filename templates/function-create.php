	public function #function_name#(#function_parameters#){
#if #model_selected#
		$#name_lower#=new #name_normal#;
#set_attributes#
		$#name_lower#->save();

	#if "#request-type#"=="http"
		#if #view_selected#
		return view("#folder#.#view#");
		#else
		return back();
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
