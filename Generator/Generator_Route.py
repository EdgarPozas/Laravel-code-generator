from Parser import parse_template,write_template
from Additional import _delete_files,_create_str_array
import os
			
class Generator_Route():

	def create_route(self,_controllers):
		s_route=""
		controllers=_controllers[:]

		if self.login:
			for controller_login in self.controllers_login:
				controllers.append(controller_login)

		for controller in controllers:			
			s_route+=self._create_str_route(controller)+"\n"

		values_route={
			"routes":s_route
		}

		content_file=parse_template("./templates/web.php",values_route)
		write_template(self.project_path_routes+"/web.php",content_file)

		print("Web file changed")

		

	def _create_str_route(self,controller):
		s_route=""
		route_template=""

		for method in controller["methods"]:
			s_middlewares=""

			if "middlewares" in method.keys():
				route_template='Route::#method#("#route#","#controller#@#function#")->middleware(#middlewares#);\n'
				s_middlewares=_create_str_array(method["middlewares"])
			else:
				route_template='Route::#method#("#route#","#controller#@#function#");\n'
			
			values={
				"method":method["method"].lower(),
				"route":method["route"],
				"controller":controller["name"],
				"function":method["name"],
				"middlewares":s_middlewares
			}
			s_route+=parse_template(route_template,values,False)
		return s_route