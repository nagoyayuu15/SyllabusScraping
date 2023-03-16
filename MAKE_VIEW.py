import os
import glob
import json

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
	json_loder = make_json_loader()
	integrate_json(json_loder)

def integrate_json(json_loder):
	global comparisons
	item_order=[]
	first_item,first_item_name = next(json_loder)
	item_order.append(first_item_name)
	structure = {row_label:[row_value] for row_label,row_value in first_item.items()}
	omitted_elements={}
	for item,item_name in json_loder:
		item_order.append(item_name)
		key_differ = set(item.keys()) - set(structure.keys())
		if key_differ:
			omitted_elements[item_name]={key:item[key] for key in key_differ}
		for row_label in structure.keys():
			if row_label in item:
				structure[row_label].append(item[row_label])
			else:
				structure[row_label].append(None)	

def make_json_loader():
	for item in comparisons:
		with open(item,"r") as opened_file:
			loaded_json = json.load(opened_file)
		yield loaded_json,item

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

main()