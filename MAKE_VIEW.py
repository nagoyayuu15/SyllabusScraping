import os
import glob
import json
import collections

HTMLSRC="""
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<link rel="stylesheet" href="./VIEW.css">
</head>
<body>
	{}
</body>
</html>
""".replace("\t","").replace("\n","")
AUTO_SETTING=True

comparisons = []

def main():
	while True:
		call_events(listen_input())

def listen_input():
	print("----listen-input----")
	print("add files to comparison:a")
	print("remove files from comparison:r")
	print("show current registered files:s")
	print("make html with current setting:m")
	print("exit:e")
	print("----listen-input----")
	return input("command:")

def add():
	global comparisons
	print("----add----")
	print("your input is being passed to glob.glob(*) directly.")
	print(f"current directory is {os.getcwd()}.")
	print("the results is being added to the comparision list.")
	print("----add----")
	comparisons += glob.glob(input("glob.glob(\"*\"):"))
	print("done.")

def remove():
	global comparisons
	print("----remove----")
	print("your input is being passed to glob.glob(*) directly.")
	print(f"current directory is {os.getcwd()}.")
	print("the results is being subtracted from the comparision list if any.")
	print("----remove----")
	subtracters = glob.glob(input("glob.glob(\"*\"):"))
	for sub in subtracters:
		if sub in comparisons:
			comparisons.remove(sub)
	print("done.")

def show():
	global comparisons
	print("----show----")
	print("all items which included in the comparison list are show below.")
	for item in comparisons:
		print(item)
	print("----show----")
	print("done.")

def make():
	global comparisons
	print("----make----")
	json_loder = make_json_loader()
	structure,omitted = integrate_json(json_loder)
	structure = integrate_omitted_elements(structure,omitted)
	table_src = generate_table(structure)
	htm = HTMLSRC.format(table_src)
	if AUTO_SETTING:
		name = "VIEW"
	else:
		name = input("save as...:")
	with open(f"./{name}.html","w",encoding="utf-8") as f:
		f.write(htm)
	print("check VIEW.html")
	print("----make----")
	print("done.")

def integrate_omitted_elements(structure,omitted):
	new_keys = set()
	for omitted_infomations in omitted.values():
		new_keys.add(*omitted_infomations.keys())
	for new_key in new_keys:
		structure[new_key] = []
		for item in structure["ITEM_ID"]:
			if not item in omitted:
				structure[new_key].append(None)
			elif not new_key in omitted[item]:
				structure[new_key].append(None)
			else:
				structure[new_key].append(omitted[item][new_key])
	return structure
def generate_tr(td_list,header=None):
	result = "<tr class=\"{}\">".format(header)
	if header is not None:
		result += "<th class=\"{}\">{}</th>".format(header,header)
	toggle = False
	for td in td_list:
		if toggle:
			result += "<td class=\"{} even\">{}</td>".format(header,td)
		else:
			result += "<td class=\"{} odd\">{}</td>".format(header,td)
		toggle = not toggle
	result += "</tr>"
	return result
def generate_table(structure:dict):
	result="<table><thead></thead><tbody>"
	for header in structure:
		result += generate_tr(structure[header],header)
	result += "</tbody><tfoot></tfoot></table>"
	return result

def integrate_json(json_loder):
	global comparisons
	first_item = next(json_loder)
	structure=collections.OrderedDict()
	for row_label,row_value in first_item.items():
		structure[row_label]=[row_value] 
	structure.move_to_end("ITEM_ID",last=False)
	omitted_elements={}
	for item in json_loder:
		key_differ = set(item.keys()) - set(structure.keys())
		if key_differ:
			omitted_elements[item["ITEM_ID"]]={key:item[key] for key in key_differ}
		for row_label in structure.keys():
			if row_label in item:
				structure[row_label].append(item[row_label])
			else:
				structure[row_label].append(None)
	return structure,omitted_elements

def make_json_loader():
	for item in comparisons:
		with open(item,"r") as opened_file:
			loaded_json = json.load(opened_file)
		for key in [unpack for unpack in loaded_json.keys()]:
			loaded_json[key.replace(" ","_").replace("\n","<br>").replace("\t","    ")] = loaded_json.pop(key).replace("\n","<br>").replace("\t","    ")
		loaded_json["ITEM_ID"] = item.split("/")[-1].split(".")[0]
		yield loaded_json
def call_events(inp):
	if inp == "a":
		add()
	elif inp == "r":
		remove()
	elif inp == "s":
		show()
	elif inp == "m":
		make()
	elif inp == "e":
		exit()
	else:
		print("unknown command.")

if AUTO_SETTING:
	comparisons += glob.glob("./Comparision/*")
	make()
else:
	main()