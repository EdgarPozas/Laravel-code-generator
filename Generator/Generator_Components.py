from Parser import parse_template,write_template
from Additional import _find,_create_str_array,_delete_last_char
import shutil,os

class Generator_Components():
	def create_components(self,_components,_views,_controllers,_models):
		components=_components[:]
		views=_views[:]
		models=_models[:]
		controllers=_controllers[:]

		if self.login:
			for view_login in self.views_login:
				views.append(view_login)
			for component_login in self.components_login:
				components.append(component_login)
			for controller_login in self.controllers_login:
				controllers.append(controller_login)

		path_template_app="./templates/app.js"
		content_file=parse_template(path_template_app,{})
		write_template(self.project_path_resources+"/js/app.js",content_file)

		component_path=self.project_path_resources+"/js/components"

		if os.path.exists(component_path):
			shutil.rmtree(component_path)

		os.makedirs(component_path)

		for component in components:
			view_selected=self._find_view_by_component(views,component)
			if not view_selected:
				continue

			project_component_d_path=self.project_path_resources+"/js/components/{0}".format(view_selected["folder"])
			if not os.path.isdir(project_component_d_path):
				os.makedirs(project_component_d_path)

			controller_selected=self._find_controller_by_view(controllers,view_selected)
			
			s_component_form=""
			s_model_json=""

			s_items=""
			s_props=""
			s_http=""

			types=["create","delete","update","select","index","login","register"]
			urls=["","","","","","",""]
			methods=["","","","","","",""]
			https=["http","http","http","http","http","http","http"]

			if component["type"]=="login":
				model={
					"name":"_login",
					"fields":[]
				}

				method=_find(controller_selected["methods"],"login","type")

				for b_params in method["body-params"]:
					model["fields"].append({
						"name":b_params,
						"type":"string"
					})

				models.append(model)
				controller_selected["model"]="_login"

			if controller_selected and "model" in controller_selected.keys():
				model_selected=_find(models,controller_selected["model"])
				if model_selected:
					s_component_form=self._create_str_component_form(model_selected)
					s_model_json=self._create_str_json(model_selected)

					for i,_type in enumerate(types):
						method=_find(controller_selected["methods"],_type,"type")
						if method:
							if _type=="select":
								urls[i]="'"+method["route"].replace("{","'+it.").replace("}","")
							else:
								urls[i]=method["route"]

							methods[i]=method["method"].lower()

							if "request-type" in method.keys():
								https[i]=method["request-type"]


			if "props" in component.keys():
				s_items= component["props"][0]
				s_props+=_create_str_array(component["props"][1:])

			values={

				"component_form":s_component_form,
				"model_json":s_model_json,
				"props":s_props,

				"url_add":urls[0],
				"url_remove":urls[1],
				"url_update":urls[2],
				"url_select":urls[3],
				"url_redirect":urls[4],
				"url_login":urls[5],

				"method_add":methods[0],
				"method_remove":methods[1],
				"method_update":methods[2],
				"method_login":methods[5],

				"add":urls[0]!="",
				"update":urls[1]!="",
				"remove":urls[2]!="",

				"http_add":https[0]=="http",
				"http_remove":https[1]=="http",
				"http_update":https[2]=="http",
				"http_login":https[5]=="http",
				
				"items":s_items,
			}

			path_template="./templates/component-blank.vue"
			if "type" in component.keys():
				if component["type"]=="complete":
					path_template="./templates/component-model-normal.vue"
				elif component["type"]=="individual":
					path_template="./templates/component-model-individual.vue"

				elif component["type"]=="login":
					path_template="./templates/component-model-login.vue"
				elif component["type"]=="register":
					path_template="./templates/component-model-register.vue"


			content_file=parse_template(path_template,values)
			write_template(project_component_d_path+"/{0}.vue".format(component["name"]),content_file)

			print("Component {0} changed".format(component["name"]))

	def _find_view_by_component(self,views,component):
		view_selected=None
		for view in views:
			if "components" in view.keys() and component["name"] in view["components"]:
				view_selected=view
				break
		return view_selected

	def _find_controller_by_view(self,controllers,view):
		controller_selected=None
		for controller in controllers:
			if "methods" in controller.keys():
				for method in controller["methods"]:
					if "view" in method.keys() and method["view"]==view["name"]:
						controller_selected=controller
						break
				if controller_selected:
					break
		return controller_selected

	def _create_str_component_form(self,model_selected):
		s_component_form=""
		for field in model_selected["fields"]:
			if field["type"]=="increments":
				continue
			s_component_form+="\t\t\t\t<label>{0}</label>\n".format(field["name"])

			input_template="\t\t\t\t<input type='#type#' v-model='item.#name#' value='item.#name#' name='#name#'/>\n"

			s_type="text"
			if field["type"]=="integer":
				s_type="number"

			values={
				"type":s_type,
				"name":field["name"]
			}

			s_component_form+=parse_template(input_template,values,False)
		s_component_form=_delete_last_char(s_component_form,["\n"])
		return s_component_form

	def _create_str_json(self,model_selected):
		s_component_json="{"
		for attribute in model_selected["fields"]:
			if attribute["type"]=="increments":
				continue
			s_component_json+="'{0}':'',".format(attribute["name"])
		
		return _delete_last_char(s_component_json)+"}"

	def create_nav_bar(self,_controllers):
		controllers=_controllers[:]

		component_path=self.project_path_resources+"/js/components/navigation-bar"

		if os.path.exists(component_path):
			shutil.rmtree(component_path)

		os.makedirs(component_path)

		s_navigation_controller=""
		for controller in controllers:
			for method in controller["methods"]:
				if "type" in method.keys() and method["type"]=="index":
					s_navigation_controller+="{"
					s_navigation_controller+='"name":"{0}","url":"{1}"'.format(controller["name"],method["route"])
					s_navigation_controller+="},"
		s_navigation_controller=_delete_last_char(s_navigation_controller)
		values={
			"navigation_controllers":s_navigation_controller,
			"use_login":self.login
		}

		content_file=parse_template("./templates/component-navigation-bar.vue",values)
		write_template(component_path+"/navigation-bar.vue",content_file)
		print("Component {0} changed".format("navigation-bar"))



