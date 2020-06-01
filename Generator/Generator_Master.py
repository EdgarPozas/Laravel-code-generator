class Generator_Master(object):
	def __init__(self, project_path,project_name):
		self.project_path=project_path
		self.project_name=project_name
		self.project_path_full=self.project_path+self.project_name
		self.project_path_app=self.project_path_full+"/app"
		self.project_path_resources=self.project_path_full+"/resources"
		self.project_path_routes=self.project_path_full+"/routes"
		self.project_path_migrations=self.project_path_full+"/database/migrations"
		self.login=False
		