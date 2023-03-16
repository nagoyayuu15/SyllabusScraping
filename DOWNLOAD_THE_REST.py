import glob
import os
import time
import requests

#CURRENT_DIRECTORY:https://syllabus.adm.nagoya-u.ac.jp/data/2023/
DATEBASES_CURRENT="https://syllabus.adm.nagoya-u.ac.jp/data/2023/"

syllabus_lists = glob.glob("./Syllabus/*")
query_list = dict()

the_number_of_elements = 0
for syllabus_list in syllabus_lists:
	undownloaded_files = glob.glob(syllabus_list+"/*.undownloaded")
	query_list[syllabus_list[11:]]=[file[1+len(syllabus_list):][:-13] for file in undownloaded_files]
	the_number_of_elements += len(query_list[syllabus_list[11:]])
print(query_list)

print("now,requests are about to be sent.it will take you longer than {} minutes.\
\nAfter you interrupt this process,the rest of HTMs can be downloaded with THIS python file.".format(int(2*the_number_of_elements/60)))

list_count=0
the_number_of_list = len(query_list)

for _list,value in query_list.items():
	list_count+=1

	syllabus_count=0
	the_number_of_syllabus_in_the_list = len(value)
	for url in value:
		syllabus_count+=1
		print(f"sending query for {DATEBASES_CURRENT+url}...")
		result = requests.get(DATEBASES_CURRENT+url,timeout=(3.0,7.5))
		result.encoding = result.apparent_encoding
		print(f"{_list}/{url} was downloaded.")

		with open(f"./Syllabus/{_list}/{url}","w") as file:
			file.write(result.text)
		print(f"{_list}/{url} was written down.")
		os.remove(f"./Syllabus/{_list}/{url}.undownloaded")
		print(f"progress:{syllabus_count}/{the_number_of_syllabus_in_the_list}<-{list_count}/{the_number_of_list}")
		time.sleep(2)

input("done")