import os
from Parser import parse_template,write_template

def _delete_files(path,excludes=[],extension=".php",equals=False):
	model_files=filter(lambda y: y !="" ,[x if extension in x else "" for x in os.listdir(path)])
	for exclude in excludes:
		for file in model_files:
			if equals:
				if exclude == file:
					model_files.remove(file)
			else:
				if exclude in file:
					model_files.remove(file)
	map(lambda y: os.remove(path+"/"+y),model_files)

def _create_str_array(array):
	s_values=""
	for value in array:
		s_values+="'"+value+"',"

	return _delete_last_char(s_values)

def _delete_last_char(string,characters=[","]):
	for char in characters:
		if string!="":
			if string[len(string)-1]==char:
				string=string[:-1]
		else:
			break
	return string


def _find(arr,find,key="name"):
	for _item in arr:
		if _item[key]==find:
			 return _item
	return None


