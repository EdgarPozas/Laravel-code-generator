from Parser import parse_template,write_template

def _create_str_array(array):
	s_values=""
	for value in array:
		s_values+="'"+value+"',"

	if len(s_values)>0:
		s_values=s_values[:-1]
	return s_values

def _create_str_migration(model):
	s_migration_content=""
	for attribute in model["attributes"]:

		migration_template="\t\t\t$table->{{type}}('{{name}}'){{constraint}};\n"

		s_constraint=""

		if "constraint" in attribute.keys():
			for contraint in attribute["constraint"]:
				s_constraint+="->"+contraint;

		values_migration={
			"type":attribute["type"],
			"name":attribute["name"],
			"constraint":s_constraint
		}

		s_migration_content+=parse_template(migration_template,values_migration,False)

		if "references" in attribute.keys():
			references=attribute["references"]
			references_template="\t\t\t$table->foreign('{{field_1}}')->references('{{field_2}}')->on('{{table}}');\n"
			
			values_references={
				"field_1":attribute["name"],
				"field_2":references["field"],
				"table":references["table_name"].lower()+"s"
			}

			if "strong" in references.keys():
				if not references["strong"]:
					s_migration_content+=parse_template(references_template,values_references,False)
			else:
				s_migration_content+=parse_template(references_template,values_references,False)

	if s_migration_content!="":
		s_migration_content=s_migration_content[:-1]
	return s_migration_content

def _create_str_imports(model):
	s_models="use App\\{0};\n".format(model["table_name"])
	return s_models

def _create_str_route(controller):
	s_route=""

	route_template="Route::{{method}}(\"{{route}}\",\"{{controller}}@{{function}}\");\n"

	for method in controller["methods"]:
		values={
			"method":method["method"].lower(),
			"route":method["route"],
			"controller":controller["name"],
			"function":method["function"]
		}
		s_route+=parse_template(route_template,values,False)
	return s_route

def _create_str_parameters(method):
	s_parameters=""
	if method["method"]=="POST":
		s_parameters+="Request $request,"

	if "parameters" in method.keys():
		for parameter in method["parameters"]:
			s_parameters+="$"+parameter+","

	if s_parameters!="":
		if s_parameters[len(s_parameters)-1]==",":
			s_parameters=s_parameters[:-1]
	return s_parameters

def _create_str_body_method(method,model_selected):
	s_body_method=""

	if "code" in method.keys():
		s_body_method+=method["code"]+"\n"


	if method["route"]=="/":
		s_body_method+="return view('index.index');"
	
	elif method["function"]=="index":
		if model_selected:
			s_body_method+="${0}s={1}::all();\n".format(model_selected["table_name"].lower(),model_selected["table_name"])
			s_body_method+="\t\treturn view('{0}.{0}',['{0}s'=>${0}s]);".format(model_selected["table_name"].lower())
	elif method["function"]=="select":
		if model_selected:
			s_body_method+=_create_str_find_one(model_selected,method,True)+"\n"
			s_body_method+="\t\treturn view('{0}.{0}-individual',['{0}'=>${0}]);".format(model_selected["table_name"].lower())
	elif method["function"]=="create":
		if model_selected:
			s_body_method+="${0}= new {1};\n".format(model_selected["table_name"].lower(),model_selected["table_name"])
			
			s_body_method+=_create_str_set_attributes(model_selected)

			s_body_method+="\t\t${0}->save();\n".format(model_selected["table_name"].lower())
			
			if "attributes" in  model_selected.keys():
				for attribute in model_selected["attributes"]:
					if "primary" in attribute.keys():
						if attribute["primary"]:
							if attribute["name"]!="id":
								s_body_method+="\t\t"+_create_str_find_one(model_selected,{"id":attribute["name"]},True)+"\n"
								
			s_body_method+="\t\treturn response()->json(['code'=>200,'item'=>${0}]);".format(model_selected["table_name"].lower())
	elif method["function"]=="update":
		if model_selected:
			s_body_method+=_create_str_find_one(model_selected,method,False)+"\n"

			s_body_method+=_create_str_update(model_selected)+"\n"

			s_body_method+="\t\treturn response()->json(['code'=>200,'item'=>${0}]);".format(model_selected["table_name"].lower())
	elif method["function"]=="delete":
		if model_selected:
			s_body_method+=_create_str_find_one(model_selected,method,False)+"\n"
			s_body_method+="\t\t${0}->delete();\n".format(model_selected["table_name"].lower())

			s_body_method+="\t\treturn response()->json(['code'=>200]);"

	return s_body_method

def _create_str_find_one(model_selected,method,first):
	s_methods="${0}={1}::".format(model_selected["table_name"].lower(),model_selected["table_name"])

	if "parameters" in method.keys():
		for param in method["parameters"]:
			s_methods+="where('{0}','=',${0})->".format(param)
	if "body" in method.keys():
		for param in method["body"]:	
			s_methods+="where('{0}','=',$request->{0})->".format(param)

	if "id" in method.keys():
		s_methods+="where('{0}','=',${1}->id)->".format(method["id"],model_selected["table_name"].lower())


	s_methods=s_methods[:-2]
	if first:
		s_methods+="->first();"
	else:
		s_methods+=";"
	return s_methods

def _create_str_update(model_selected):
	update_template="\t\t${{variable}}->update([{{content}}]);"

	s_content=""
	for attribute in model_selected["attributes"]:
		if attribute["type"]=="increments":
			continue
		s_content+="'{0}'=>$request->{0},".format(attribute["name"])

	s_content=s_content[:-1]
	
	values={
		"variable":model_selected["table_name"].lower(),
		"content":s_content
	}
	content_file=parse_template(update_template,values,False)
	return content_file

def _create_str_set_attributes(model_selected):
	s_attributes=""
	for attribute in model_selected["attributes"]:
		if attribute["type"]=="increments":
			continue
		attribute_template="\t\t${{variable}}->{{value}}=$request->{{value}};\n"
		values={
			"variable":model_selected["table_name"].lower(),
			"value":attribute["name"]
		}
		s_attributes+=parse_template(attribute_template,values,False)
	return s_attributes

def _find_model(models,model):
	model_selected=None
	for _model in models:
		if _model["table_name"]==model:
			model_selected=_model
			break
	return model_selected

def _create_str_body_view(view):
	s_body_view=""
	for component in view["components"]:
		s_component_view_template="\t<{{name}} {{props}}></{{name}}>\n"

		s_props=""
		if "props" in component.keys(): 
			for prop in component["props"]:
				s_props+=":"+prop+"={{$"+prop+"}}"

		values={
			"name":component["name"],
			"props":s_props
		}

		s_body_view+=parse_template(s_component_view_template,values,False)
	s_body_view=s_body_view[:-1]
	return s_body_view

def _create_str_navigation(controllers):
	s_navigation_controllers=""
	for controller in controllers:
		for method in controller["methods"]:
			if method["function"]=="index":
				s_navigation_controllers+="{"
				s_navigation_controllers+="url:'{0}',name:'{1}'".format(method["route"],controller["name"])
				s_navigation_controllers+=",},"
				break
	if len(s_navigation_controllers)>0:
		s_navigation_controllers=s_navigation_controllers[:-3]+"}"

	return s_navigation_controllers

def _find_controller(controllers,controller):
	controller_selected=None
	for _controller in controllers:
		if _controller["name"]==controller:
			controller_selected=_controller
			break
	return controller_selected

def _find_method(methods,method):
		method_selected=None
		for _method in methods:
			if _method["function"]==method:
				method_selected=_method
				break
		return method_selected

def _create_str_component_form(model_selected):
	s_component_form=""
	for attribute in model_selected["attributes"]:
		if attribute["type"]=="increments":
			continue

		s_component_form+="\t\t\t<label>{0}</label>\n".format(attribute["name"])

		input_template="\t\t\t<input type='{{type}}' v-model='item_actual.{{name}}' value='item_actual.{{name}}' name='{{name}}'/>\n"

		s_type="text"
		if attribute["type"]=="integer":
			s_type="number"

		values={
			"type":s_type,
			"name":attribute["name"]
		}

		s_component_form+=parse_template(input_template,values,False)

	return s_component_form

def _create_str_json(model_selected):
	s_component_json=""
	for attribute in model_selected["attributes"]:
		if attribute["type"]=="increments":
			continue
		s_component_json+="'{0}':'',".format(attribute["name"])
	if len(s_component_json)>0:
		s_component_json=s_component_json[:-1]
	return s_component_json

def _create_str_link(method_select):
	url_item="'"+method_select["route"].replace("{","'+item.").replace("}","")
	link_template='<a :href="{0}">Ver</a>'.format(url_item)
	return link_template