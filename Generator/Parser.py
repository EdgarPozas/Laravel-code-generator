
def parse_template(path_or_content,values,file=True):
	content=""
	if file:
		with open(path_or_content,"r") as f_template:
			content=f_template.read()
	else:
		content=path_or_content
	for (k,v) in values.items():
		executor=str(v)
		content=content.replace("#"+k+"#",executor)
	
	return parse_if(content)

def parse_if(content):
	if type(content) is str:
		content=content.split("\n")
	count_by="\t"
	line_number=-1
	for ln in content:

		line_number+=1
		line=content[line_number]

		if "#if" in line:
			line_if=line_number
			level_if=list(line).count(count_by)
			expression=line.replace("#if","") #.replace("}}","")
			result=eval(expression)
			line_if_aux=-1

			for next_line in content[line_if:]:
				line_if_aux+=1
				level_end=list(next_line).count(count_by)
				line_endif=line_if+line_if_aux
				
				if level_if==level_end:
					if "#else" in next_line:

						line_else=line_endif

						line_endif=line_if-1
						for next_endif in content[line_if:]:
							line_endif+=1
							level_t_end=list(next_endif).count(count_by)
							if "#endif" in next_endif and level_t_end==level_if:
								break
						if result:
							delete_statement(content,line_else,line_endif)
							del content[line_if]
						else:
							del content[line_endif]
							delete_statement(content,line_if,line_else)
						break
					elif "#endif" in next_line:
						if result:
							keep_statement(content,line_if,line_endif)
						else:
							delete_statement(content,line_if,line_endif)
						break
			line_number-=1

	content_process=""

	for line in content:
		content_process+=line+"\n"
		
	content_process=content_process[:-1]
	content=content_process
	return content

def write_template(path,content):
	with open(path,"w") as f:
		f.write(content)

def print_content(content):
	i=-1
	for line in content:
		i+=1
		print(i,line)

def delete_statement(content,start,last):
	for i in range(last,start-1,-1):
		del content[i]

def keep_statement(content,start,last):
	del content[last]
	del content[start]
