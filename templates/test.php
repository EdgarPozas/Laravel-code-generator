	public function #function_name(#function_parameters){
1
#if "#type"=="index"
2
	#if #model_selected
3
		#if "#request-type"=="http"
4
		#else
5
		#endif
6
	#else
7
		#if "#request-type"=="http"
8
		#else
9
		#endif
10
	#endif
11
#endif
12
#if "#type"=="register"
13
	#if #model_selected
14
		#if "#request-type"=="http"
15
		#else
16
		#endif
17
	#else
18
		#if "#request-type"=="http"
19
		#else
20
		#endif
21
	#endif
22
#endif
23
	}
