from Parser import parse_template,write_template
from Additional import _delete_files
import os

class Generator_Middlewares():
	def create_middlewares(self,_middlewares=[]):
		middlewares=_middlewares[:]
		s_middlewares=""

		excludes=[
			"Authenticate.php",
			"CheckForMaintenanceMode.php",
			"EncryptCookies.php",
			"RedirectIfAuthenticated.php",
			"TrimStrings.php",
			"TrustProxies.php",
			"VerifyCsrfToken.php"
		]

		_delete_files(self.project_path_app+"/Http/Middleware",excludes,equals=True)

		if self.login:
			for middleware_login in self.middlewares_login:
				middlewares.append(middleware_login)

		for middleware in middlewares:
			os.system("php "+self.project_path_full+"/artisan make:middleware "+middleware["name"])

			values={
				"type":'"'+middleware["type"]+'"',
				"name":middleware["name"]
			}

			content_file=parse_template("./templates/middleware.php",values)
			write_template(self.project_path_app+"/Http/Middleware/{0}.php".format(middleware["name"]),content_file)

			s_middlewares+="\t\t'{0}'=>\App\Http\Middleware\{1}::class,".format(middleware["alias"],middleware["name"])

		values={
			"middlewares":s_middlewares
		}

		content_file=parse_template("./templates/Kernel.php",values)
		write_template(self.project_path_app+"/Http/Kernel.php",content_file)