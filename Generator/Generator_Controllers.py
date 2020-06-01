from Parser import parse_template,write_template
from Additional import _delete_files,_find,_delete_last_char,_create_str_array
import os

class Generator_Controllers():
	def create_controllers(self,_controllers,_models,_views):
		controllers=_controllers[:]
		models=_models[:]
		views=_views[:]

		if self.login:
			for controller_login in self.controllers_login:
				controllers.append(controller_login)
			for view_login in self.views_login:
				views.append(view_login)

		excludes=[
			"Controller.php",
		]

		_delete_files(self.project_path_app+"/Http/Controllers/",excludes,equals=True)

		for controller in controllers:
			
			os.system("php "+self.project_path_full+"/artisan make:controller "+controller["name"])

			s_imports=""
			s_methods=""
			s_primary=""

			model_selected=None
			model_selected_aux=None
			if "model" in controller.keys():
				model_selected=_find(models,controller["model"])
				model_selected_aux=model_selected
				s_imports=self._create_str_imports(model_selected)

			for method in controller["methods"]:
				s_parameters=self._create_str_parameters(method)

				if "use-model" in method.keys() and not method["use-model"]:
					model_selected=None
				else:
					model_selected=model_selected_aux

				if model_selected:
					for field in model_selected["fields"]:
						pass

				values_method={
					"function_name":method["name"],
					"function_parameters":s_parameters,

					"type":"blank",
					"model_selected":model_selected,
					"primary":s_primary,

					"name_lower":None,
					"name_normal":None,
					"request-type": "http",
					"view_selected":None,
					"folder":None,
					"view":None,

					"credentials":None,
					"set_attributes":None,
					"find":None,
					"update":None
				}

				if model_selected:
					values_method["name_lower"]=model_selected["name"].lower()
					values_method["name_normal"]=model_selected["name"]

				if "request-type" in method.keys():
					values_method["request-type"]=method["request-type"]

				if "view" in method.keys():
					view_selected=_find(views,method["view"])
					values_method["view_selected"]=view_selected
					if view_selected:
						values_method["folder"]=view_selected["folder"]
						values_method["view"]=view_selected["name"]
				

				path_template="./templates/function-blank.php"
				if "type" in method.keys():
					path_template="./templates/function-{0}.php".format(method["type"])
					if method["type"]=="login":
						if "body-params" in method.keys():
							values_method["credentials"]=_create_str_array(method["body-params"])
					elif method["type"]=="register" or method["type"]=="create" :
						values_method["set_attributes"]=self._create_str_set_attributes(model_selected)
					elif method["type"]=="delete" or method["type"]=="update" or method["type"]=="select":
						if method["type"]=="update":
							values_method["update"]=self._create_str_update(model_selected)
						values_method["find"]=self._create_str_find_one(model_selected,method)

				s_methods+=parse_template(path_template,values_method)

			s_methods=_delete_last_char(s_methods,["\n"])

			values_controller={
				"imports":s_imports,
				"name":controller["name"],
				"methods":s_methods
			}

			content_file=parse_template("./templates/controller.php",values_controller)
			write_template(self.project_path_app+"/Http/Controllers/{0}.php".format(controller["name"]),content_file)

			print("Controller {0} changed".format(controller["name"]))

	
	def _create_str_imports(self,model):
		s_models=""
		if model:
			s_models="use App\\{0};\n".format(model["name"])
		return s_models

	def _create_str_parameters(self,method):
		s_parameters=""
		methods_use_request=["login","register","logout","create","update","delete"]
		methods_types_use_request=["POST","PUT","DELETE"]
		if method["method"] in methods_types_use_request or method["type"] in methods_use_request:
			s_parameters+="Request $request,"

		if "path-params" in method.keys():
			for parameter in method["path-params"]:
				s_parameters+="$"+parameter+","

		return _delete_last_char(s_parameters)
		
	def _create_str_find_one(self,model_selected,method):
		s_methods=""
		if "path-params" in method.keys():
			for param in method["path-params"]:
				s_methods+="where('{0}',${0})->".format(param)
		if "body-params" in method.keys():
			for param in method["body-params"]:	
				s_methods+="where('{0}',$request->{0})->".format(param)

		if "id" in method.keys():
			s_methods+="where('{0}',${1}->id)->".format(method["id"],model_selected["name"].lower())
		s_methods=s_methods[:-2]
		return s_methods

	def _create_str_update(self,model_selected):
		s_content=""
		for field in model_selected["fields"]:
			if field["type"]=="increments":
				continue
			s_content+="'{0}'=>$request->{0},".format(field["name"])

		s_content=_delete_last_char(s_content)
		return s_content

	def _create_str_set_attributes(self,model_selected):
		s_attributes=""
		if model_selected:
			for field in model_selected["fields"]:
				if field["type"]=="increments":
					continue
				if field["name"]=="password":
					s_attributes+="\t\t${0}->{1}=Hash::make($request->{1});\n".format(model_selected["name"].lower(),field["name"])
				else:	
					s_attributes+="\t\t${0}->{1}=$request->{1};\n".format(model_selected["name"].lower(),field["name"])
		s_attributes=_delete_last_char(s_attributes,["\n"])
		return s_attributes