import os
from Generator_Master import *
from Generator_Models import *
from Generator_Controllers import *
from Generator_Route import*
from Generator_Views import *
from Generator_Components import *
from Generator_Middlewares import *

class Generator(Generator_Master,Generator_Models,Generator_Controllers,Generator_Views,Generator_Components,Generator_Route,Generator_Middlewares):
	def __init__(self,project_path,project_name):
		Generator_Master.__init__(self,project_path,project_name)

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

	def use_login(self,use):
		self.login=use
		if not self.login:
			return
		self.middlewares_login=[
			{
				"name":"LoginMiddleware",
				"alias":"login",
				"type":"login"
			}
		]
		self.controllers_login=[
			{
				"name":"LoginController",
				"methods":[
					{
						"name":"index",
						"route":"/login",
						"method":"GET",
						"type":"index",
						"view":"login"
					},
					{
						"name":"login",
						"route":"/login",
						"method":"POST",
						"body-params":["email","password"],
						"type":"login",
						"request-type":"http"
					},
					{
						"name":"logout",
						"route":"/logout",
						"method":"GET",
						"type":"logout",
						"request-type":"http"
					}
				]
			},
			{
				"name":"RegisterController",
				"model":"User",
				"methods":[
					{
						"name":"index",
						"route":"/register",
						"method":"GET",
						"type":"index",
						"view":"register",
						"use-model":False
					},
					{
						"name":"register",
						"route":"/register",
						"method":"POST",
						"type":"create",
						"request-type":"http"
					}
				]
			},
		]
		self.views_login=[
			{
				"name":"login",
				"folder":"login",
				"components":["login-form"]
			},
			{
				"name":"register",
				"folder":"register",
				"components":["register-form"]
			},
		]
		self.components_login=[
			{
				"name":"login-form",
				"type":"login"
			},
			{
				"name":"register-form",
				"type":"register"
			}
		]
