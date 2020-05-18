import os
import shutil
from Parser import parse_template,write_template
from Additional import _find_model,_find_method,_find_controller,_create_str_body_middleware
from Additional import _create_str_find_one,_create_str_array,_create_str_migration
from Additional import _create_str_route,_create_str_imports,_create_str_parameters
from Additional import _create_str_body_method,_create_str_body_view,_create_str_navigation
from Additional import _create_str_component_form,_create_str_json,_create_str_link

class Generator:
	"""docstring for Generator"""
	def __init__(self, project_path,project_name):
		self.project_path=project_path
		self.project_name=project_name
		self.project_path_full=self.project_path+self.project_name

	def init(self,vue=False):
		os.system("rm -d -rf "+self.project_path_full)
		os.system('composer create-project --prefer-dist laravel/laravel '+self.project_path_full)

		normal_path = os.getcwd()
		if vue:
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

	def create_model(self,models):
		self.models=models

		for model in self.models:

			os.system("php "+self.project_path_full+"/artisan make:model "+model["table_name"])

			arr=[x["name"] for x in model["attributes"]]

			s_fillable=_create_str_array(arr)
			s_hidden=""
			s_casts=""
			s_foreign=""
			s_timestamps=""

			for attribute in model["attributes"]:
				if attribute["type"]!="timestamps":
					s_timestamps="public $timestamps = false;" 
				if "references" in attribute.keys():
					references=attribute["references"]
					values_function={
						"function_name":references["table_name"].lower(),
						"function_parameters":"",
						"body":"return $this->{0}('{1}')->references('{1}')->on('{2}');".format(references["type"],references["field"],references["table_name"])
					}

					s_foreign+=parse_template("./templates/function.php",values_function)

			values={
				"name":model["table_name"],
				"fillable":s_fillable,
				"hidden":s_hidden,
				"casts":s_casts,
				"foreign":s_foreign,
				"timestamps":s_timestamps
			}

			content_file=parse_template("./templates/model.php",values)
			write_template(self.project_path_full+"/app/{0}.php".format(model["table_name"]),content_file)

			print("Model {0} changed".format(model["table_name"]))

	def create_migration(self,models):
		self.models=models

		for model in self.models:

			migration_name="create_"+model["table_name"].lower()+"s_table"

			if not (migration_name=="create_users_table"):
				os.system("php "+self.project_path_full+"/artisan make:migration "+migration_name)
			
			s_migration_content=_create_str_migration(model)

			values={
				"name":"Create{0}sTable".format(model["table_name"].replace("_","")),
				"migration_name":model["table_name"].lower()+"s",
				"migration_content":s_migration_content
			}

			s_migration=parse_template("./templates/migration.php",values)

			migrations = os.listdir(self.project_path_full+"/database/migrations")

			for migration in migrations:
				if migration_name in migration:

					write_template(self.project_path_full+"/database/migrations/{0}".format(migration),s_migration)

					print("Migration {0} changed".format(migration))

		os.system("php "+self.project_path_full+"/artisan migrate")
		
	def create_controller(self,controllers,models):
		self.controllers=controllers
		self.models=models

		for controller in self.controllers:
			
			os.system("php "+self.project_path_full+"/artisan make:controller "+controller["name"])

			s_imports=""
			s_methods=""

			model_selected=None
			if "model" in controller.keys():
				model_selected=_find_model(self.models,controller["model"])
				if model_selected:
					s_imports=_create_str_imports(model_selected)

			for method in controller["methods"]:

				s_parameters=_create_str_parameters(method)
				s_body=_create_str_body_method(method,model_selected)

				values_method={
					"function_name":method["function"],
					"function_parameters":s_parameters,
					"body":s_body
				}

				s_methods+=parse_template("./templates/function.php",values_method)

			values_controller={
				"imports":s_imports,
				"name":controller["name"],
				"methods":s_methods
			}

			content_file=parse_template("./templates/controller.php",values_controller)
			write_template(self.project_path_full+"/app/Http/Controllers/{0}.php".format(controller["name"]),content_file)

			print("Controller {0} changed".format(controller["name"]))

	def create_route(self,controllers):
		self.controllers=controllers

		s_route=""
		for controller in self.controllers:			
			s_route+=_create_str_route(controller)+"\n"

		values_route={
			"routes":s_route
		}

		content_file=parse_template("./templates/web.php",values_route)
		write_template(self.project_path_full+"/routes/web.php",content_file)

		print("Web file changed")

	def create_views(self,views):
		self.views=views

		views_project_path=self.project_path_full+"/resources/views"
		if os.path.exists(views_project_path):
			shutil.rmtree(views_project_path)
		
		os.makedirs(views_project_path+"/templates")
		
		shutil.copyfile("./templates/base.blade.php",views_project_path+"/templates/base.blade.php")

		for view in self.views:
			views_project_d_path=views_project_path+"/"+view["folder"]

			if not os.path.isdir(views_project_d_path):
				os.makedirs(views_project_d_path)

			s_components_view=""
			s_components_view_script=""

			if "components" in view.keys():
				s_components_view=_create_str_body_view(view)

			values_views={
				"components":s_components_view,
				"script_components":s_components_view_script,
				"title":view["name"]
			}

			content_file=parse_template("./templates/view.blade.php",values_views)
			write_template(views_project_d_path+"/{0}.blade.php".format(view["name"]),content_file)

			print("View {0} generated".format(view["name"]))

	def create_components(self,views,controllers,models):
		self.views=views
		self.models=models
		self.controllers=controllers
	
		component_path=self.project_path_full+"/resources/js/components"
		if os.path.exists(component_path):
			shutil.rmtree(component_path)

		os.makedirs(component_path+"/default")

		s_navigation_controllers=_create_str_navigation(self.controllers)

		values={
			"navigation_controllers":s_navigation_controllers
		}

		content_file=parse_template("./templates/navigation-bar.vue",values)
		write_template(component_path+"/default/navigation-bar.vue",content_file)

		s_component_app=""
		for view in self.views:
			if "components" in view.keys():
				project_component_d_path=self.project_path_full+"/resources/js/components/{0}".format(view["folder"])
				
				if not os.path.isdir(project_component_d_path):
					os.makedirs(project_component_d_path)

				url_add=""
				url_remove=""
				url_update=""
				url_item=""
				url_redirect=""

				if "controller" in view.keys():
					controller_selected=_find_controller(self.controllers,view["controller"])
					if controller_selected:
						method_add=_find_method(controller_selected["methods"],"create")
						if method_add:
							url_add=method_add["route"]
						method_remove=_find_method(controller_selected["methods"],"delete")
						if method_remove:
							url_remove=method_remove["route"]
						method_update=_find_method(controller_selected["methods"],"update")
						if method_update:
							url_update=method_update["route"]
						method_select=_find_method(controller_selected["methods"],"select")
						if method_select:
							url_item=_create_str_link(method_select)
						method_index=_find_method(controller_selected["methods"],"index")
						if method_index:
							url_redirect=method_index["route"]

				for component in view["components"]:
					s_items=""
					s_props=""
					s_component_form=""
					s_component_json=""
					
					s_component_app+="Vue.component('{0}', require('./components/{1}/{0}.vue').default);\n".format(component["name"],view["folder"])
				
					if "props" in component.keys():
						s_items= component["props"][0]
						s_props=_create_str_array(component["props"])


					if "model" in component.keys(): 
						model_selected=_find_model(self.models,component["model"])
						if model_selected:
							s_component_form+=_create_str_component_form(component,model_selected)
							s_component_json+=_create_str_json(model_selected)

						values_component={
							"component_form":s_component_form,
							"items":s_items,
							"props":s_props,
							"component_json":s_component_json,
							"url_add":url_add,
							"url_remove":url_remove,
							"url_update":url_update,
							"url_item":url_item,

							"url_redirect":url_redirect
						}

						name_template="./templates/component-model.vue"
						if component["type"]=="individual":
							name_template="./templates/component-model-individual.vue"
						elif component["type"]=="login":
							name_template="./templates/login.vue"
						elif component["type"]=="register":
							name_template="./templates/register.vue"

						content_file=parse_template(name_template,values_component)
						write_template(project_component_d_path+"/{0}.vue".format(component["name"]),content_file)
					else:
						values_component={
							"props":s_props
						}
						content_file=parse_template("./templates/component-normal.vue",values_component)
						write_template(project_component_d_path+"/{0}.vue".format(component["name"]),content_file)

					print("Component {0} generated".format(component["name"]))


		values={
			"components":s_component_app
		}

		content_file=parse_template("./templates/app.js",values)
		write_template(self.project_path_full+"/resources/js/app.js",content_file)

	def create_middleware(self,middlewares):
		self.middlewares=middlewares

		s_middlewares=""

		for middleware in self.middlewares:
			os.system("php "+self.project_path_full+"/artisan make:middleware "+middleware["name"])

			s_code=_create_str_body_middleware(middleware)

			values={
				"code":s_code
			}

			content_file=parse_template("./templates/middleware.php",values)
			write_template(self.project_path_full+"/app/Http/Middleware/{0}.php".format(middleware["name"]),content_file)

			s_middlewares+="\t\t'{0}'=>\App\Http\Middleware\{1}::class,".format(middleware["alias"],middleware["name"])

		values={
			"middlewares":s_middlewares
		}

		content_file=parse_template("./templates/Kernel.php",values)
		write_template(self.project_path_full+"/app/Http/Kernel.php",content_file)