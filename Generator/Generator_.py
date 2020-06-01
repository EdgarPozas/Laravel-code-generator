import os
# import shutil
# from Parser import parse_template,write_template
# from Additional import _find_model,_find_method,_find_controller,_create_str_body_middleware
# from Additional import _create_str_find_one,_create_str_array,_create_str_migration
# from Additional import _create_str_route,_create_str_imports,_create_str_parameters
# from Additional import _create_str_body_method,_create_str_body_view,_create_str_navigation
# from Additional import _create_str_component_form,_create_str_json,_create_str_link
# from Additional import _delete_files

import Generator_Models
import Generator_Components
import Generator_Controllers
import Generator_Views


class Generator(Generator_Models,Generator_Components,Generator_Controllers,Generator_Views):
	"""docstring for Generator"""
	def __init__(self, project_path,project_name):
		self.project_path=project_path
		self.project_name=project_name
		self.project_path_full=self.project_path+self.project_name

	def init(self):
		os.system("rm -d -rf "+self.project_path_full)
		os.system('composer create-project --prefer-dist laravel/laravel '+self.project_path_full)

		normal_path = os.getcwd()
		os.chdir(self.project_path_full)
		os.system('composer require laravel/ui')
		os.system('php artisan ui vue')
		os.system("npm install")
		os.chdir(normal_path)

	def set_database(self,db_name,user,password):

		values={
			"db_name":db_name,
			"db_user":user,
			"db_password":password
		}

		content=parse_template("./templates/.env",values)
		write_template(self.project_path_full+"/.env",content)

		normal_path = os.getcwd()
		os.chdir(self.project_path_full)
		os.system('php artisan key:generate')
		os.chdir(normal_path)

		print(".env changed")


	

	# def create_components(self,views,controllers,models,append=False):
	# 	self.views=views
	# 	self.models=models
	# 	self.controllers=controllers

	# 	component_path=self.project_path_full+"/resources/js/components"

	# 	if not append:
	# 		if os.path.exists(component_path):
	# 			shutil.rmtree(component_path)

	# 		self.create_navigation_bar(False)
	
	# 	s_component_app=""
	# 	for view in self.views:
	# 		if "components" in view.keys():
	# 			project_component_d_path=self.project_path_full+"/resources/js/components/{0}".format(view["folder"])
				
	# 			if not os.path.isdir(project_component_d_path):
	# 				os.makedirs(project_component_d_path)

	# 			url_add=""
	# 			url_remove=""
	# 			url_update=""
	# 			url_item=""
	# 			url_redirect=""

	# 			url_form=""
	# 			method_form=""
	# 			button=""

	# 			if "controller" in view.keys():
	# 				controller_selected=_find_controller(self.controllers,view["controller"])
	# 				if controller_selected:
	# 					method_add=_find_method(controller_selected["methods"],"create")
	# 					if method_add:
	# 						url_add=method_add["route"]
	# 					method_remove=_find_method(controller_selected["methods"],"delete")
	# 					if method_remove:
	# 						url_remove=method_remove["route"]
	# 					method_update=_find_method(controller_selected["methods"],"update")
	# 					if method_update:
	# 						url_update=method_update["route"]
	# 					method_select=_find_method(controller_selected["methods"],"select")
	# 					if method_select:
	# 						url_item=_create_str_link(method_select)
	# 					method_index=_find_method(controller_selected["methods"],"index")
	# 					if method_index:
	# 						url_redirect=method_index["route"]

	# 					method_login=_find_method(controller_selected["methods"],"login")
	# 					if method_login:
	# 						url_form=method_login["route"]
	# 						method_form=method_login["method"]
	# 						button=method_login["function"]

	# 					method_register=_find_method(controller_selected["methods"],"register")
	# 					if method_register:
	# 						url_form=method_register["route"]
	# 						method_form=method_register["method"]
	# 						button=method_register["function"]

	# 			for component in view["components"]:
	# 				s_items=""
	# 				s_props=""
	# 				s_component_form=""
	# 				s_component_json=""
					
	# 				s_component_app+="Vue.component('{0}', require('./components/{1}/{0}.vue').default);\n".format(component["name"],view["folder"])
				
	# 				if "props" in component.keys():
	# 					s_items= component["props"][0]
	# 					s_props=_create_str_array(component["props"])


	# 				if "model" in component.keys(): 
	# 					model_selected=_find_model(self.models,component["model"])
	# 					if model_selected:
	# 						s_component_form+=_create_str_component_form(component,model_selected)
	# 						s_component_json+=_create_str_json(model_selected)

	# 					values_component={
	# 						"component_form":s_component_form,
	# 						"items":s_items,
	# 						"props":s_props,
	# 						"component_json":s_component_json,
	# 						"url_add":url_add,
	# 						"url_remove":url_remove,
	# 						"url_update":url_update,
	# 						"url_item":url_item,

	# 						"url_redirect":url_redirect,

	# 						"url_form":url_form,
	# 						"method":method_form,
	# 						"button":button
	# 					}

	# 					name_template="./templates/component-model-ajax.vue"
	# 					if component["type"]=="individual":
	# 						name_template="./templates/component-model-individual.vue"
	# 					elif component["type"]=="login" or component["type"]=="register":
	# 						name_template="./templates/component-model-form.vue"

	# 					content_file=parse_template(name_template,values_component)
	

	
	# def use_login(self,models):
	# 	middlewares=[
	# 		{
	# 			"name":"LoginMiddleware",
	# 			"alias":"login",
	# 			"type":"login"
	# 		}
	# 	]
	# 	controllers=[
	# 		{
	# 			"name":"LoginController",
	# 			"model":"User",
	# 			"methods":[
	# 				{
	# 					"route":"/login",
	# 					"method":"GET",
	# 					"function":"index"
	# 				},
	# 				{
	# 					"route":"/login",
	# 					"method":"POST",
	# 					"function":"login",
	# 					"body":["email","password"],
	# 				},
	# 				{
	# 					"route":"/logout",
	# 					"method":"GET",
	# 					"function":"logout",
	# 				}
	# 			]
	# 		},
	# 	]
	# 	views=[
	# 		{
	# 			"name":"login",
	# 			"folder":"login",
	# 			"controller":"LoginController",
	# 			"components":[
	# 				{
	# 					"name":"login-form",
	# 					"type":"login",
	# 					"model":"User",
	# 					"props":["login"]
	# 				}
	# 			]
	# 		},
	# 	]
	# 	self.create_middleware(middlewares)
	# 	self.create_controller(controllers,models)
	# 	self.create_route(controllers,True)
	# 	self.create_views(views,True)
	# 	self.create_components(views,controllers,models,True)

	# def use_register(self,models):
	# 	controllers=[
	# 		{
	# 			"name":"RegisterController",
	# 			"model":"User",
	# 			"methods":[
	# 				{
	# 					"route":"/register",
	# 					"method":"GET",
	# 					"function":"index",
	# 				},
	# 				{
	# 					"route":"/register",
	# 					"method":"POST",
	# 					"function":"register",
	# 				}
	# 			]
	# 		},
	# 	]
	# 	views=[
	# 		{
	# 			"name":"register",
	# 			"folder":"register",
	# 			"controller":"RegisterController",
	# 			"components":[
	# 				{
	# 					"name":"register-form",
	# 					"type":"register",
	# 					"model":"User"
	# 				}
	# 			]
	# 		},
	# 	]
	# 	self.create_controller(controllers,models)
	# 	self.create_route(controllers,True)
	# 	self.create_views(views,True)
	# 	self.create_components(views,controllers,models,True)
	# 	