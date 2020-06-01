from Parser import parse_template,write_template
from Additional import _delete_files,_create_str_array,_delete_last_char
import os
			
class Generator_Models():
	def create_models(self,_models):
		models=_models[:]
		_delete_files(self.project_path_app)
			
		for model in models:

			model_path_full=self.project_path_app+"/{0}.php".format(model["name"])

			s_fillable=_create_str_array([x["name"] for x in model["fields"]])
			s_hidden=""
			s_casts=""
			s_foreign=""
			s_timestamps=""
			s_primary=""

			for field in model["fields"]:
				if "primary" in field.keys() and field["primary"]:
					s_primary=field["name"]	
				if "references" in field.keys():
					references=field["references"]
					values_function={
						"function_name":references["name"].lower(),
						"function_parameters":"",
						"type":"foreign",
						"reference":references["type"],
						"field":references["field"],
						"table_name":references["name"]
					}
					s_foreign+=parse_template("./templates/function-foreign.php",values_function)
			s_foreign=_delete_last_char(s_foreign,["\n"])
			values={
				"name":model["name"],
				"fillable":s_fillable,
				"hidden":s_hidden,
				"casts":s_casts,
				"foreign":s_foreign,
				"timestamps":field["type"]=="timestamps",
				"primary":s_primary
			}

			content_file=parse_template("./templates/model.php",values)
			write_template(model_path_full,content_file)

			print("Model {0} changed".format(model["name"]))


	def create_migrations(self,models,migrate=True):

		excludes=[
			"create_users_table",
			"create_failed_jobs_table"
		]

		_delete_files(self.project_path_migrations,excludes)

		for model in models:

			migration_name="create_"+model["name"].lower()+"s_table"

			if migration_name!="create_users_table":
				os.system("php "+self.project_path_full+"/artisan make:migration "+migration_name)
			
			s_migration_content=self._create_str_migration(model)

			values={
				"name":model["name"].replace("_",""),
				"migration_name":model["name"].lower(),
				"migration_content":s_migration_content
			}

			s_migration=parse_template("./templates/migration.php",values)

			migrations = os.listdir(self.project_path_migrations)

			for migration in migrations:
				if migration_name in migration:
					write_template(self.project_path_migrations+"/{0}".format(migration),s_migration)
					print("Migration {0} changed".format(migration))
					break
		if migrate:
			os.system("php "+self.project_path_full+"/artisan migrate")
		else:
			os.system("php "+self.project_path_full+"/artisan migrate:fresh")

	def _create_str_migration(self,model):
		s_migration_content=""
		for field in model["fields"]:

			migration_template='\t\t\t$table->#type#("#name#")#constraint#;\n'

			if field["type"]=="timestamps":
				migration_template="\t\t\t$table->#type#;\n"

			s_constraint=""

			if "constraint" in field.keys():
				for contraint in field["constraint"]:
					s_constraint+="->"+contraint;

			values_migration={
				"type":field["type"],
				"name":field["name"],
				"constraint":s_constraint
			}

			s_migration_content+=parse_template(migration_template,values_migration,False)

			if "references" in field.keys():
				references=field["references"]
				references_template='\t\t\t$table->foreign("#field_1#")->references("#field_2#")->on("#table#s");\n'
				
				values_references={
					"field_1":field["name"],
					"field_2":references["field"],
					"table":references["name"].lower()
				}

				if "primary" in field.keys():
					if not field["primary"]:
						s_migration_content+=parse_template(references_template,values_references,False)
				else:
					s_migration_content+=parse_template(references_template,values_references,False)

		return _delete_last_char(s_migration_content,[",","\n"])