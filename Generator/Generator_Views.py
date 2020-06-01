from Additional import _find,_delete_last_char
from Parser import parse_template,write_template
import os,shutil

class Generator_Views():
	def create_views(self,_views,_components):
		views=_views[:]
		components=_components[:]

		if self.login:
			for view_login in self.views_login:
				views.append(view_login)
			for component_login in self.components_login:
				components.append(component_login)

		views_project_path=self.project_path_resources+"/views"

		if os.path.exists(views_project_path):
			shutil.rmtree(views_project_path)
		
		os.makedirs(views_project_path+"/templates")
		values={
			"use_login":self.login
		}
		content_file=parse_template("./templates/base.blade.php",values)
		write_template(views_project_path+"/templates/base.blade.php",content_file)

		for view in views:
			views_project_d_path=views_project_path+"/"+view["folder"]

			if not os.path.isdir(views_project_d_path):
				os.makedirs(views_project_d_path)

			s_components_view=""
			s_components_view_script=""

			if "components" in view.keys():
				s_components_view=self._create_str_body_view(view,components)

			values_views={
				"components":s_components_view,
				"script_components":s_components_view_script,
				"title":view["name"]
			}

			content_file=parse_template("./templates/view.blade.php",values_views)
			write_template(views_project_d_path+"/{0}.blade.php".format(view["name"]),content_file)

			print("View {0} generated".format(view["name"]))

	def _create_str_body_view(self,view,components):
		s_body_view=""
		if "components" in view.keys():
			for component in view["components"]:
				component_selected=_find(components,component)
				if component_selected:
					s_props=""
					if "props" in component_selected.keys(): 
						for prop in component_selected["props"]:
							s_props+=":"+prop+"={{ $data }}"
					s_component_view_template="\t<{0} {1}></{0}>\n".format(component_selected["name"],s_props)
					s_body_view+=s_component_view_template
					s_body_view=_delete_last_char(s_body_view,["\n"])
		return s_body_view