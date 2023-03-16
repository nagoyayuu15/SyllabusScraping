from bs4 import BeautifulSoup as BS
import requests
import time
import glob
import os

os.makedirs("./Syllabus",exist_ok=True)

#CURRENT_DIRECTORY:https://syllabus.adm.nagoya-u.ac.jp/data/2023/
DATEBASES_CURRENT="https://syllabus.adm.nagoya-u.ac.jp/data/2023/"

ListOfSyllabusListHTM = glob.glob("./SyllabusList/*")

syllabus_url_list= dict()
the_number_of_elements = 0

for syllabus_list_htm in ListOfSyllabusListHTM:
    #open files
	with open(syllabus_list_htm,"r") as htm:
		content = htm.read()
	#make tasty soup
	soup = BS(content,features="lxml")
	#exploit syllabus urls from the soup
	syllabus_url_list[syllabus_list_htm[15:].split(".")[0]]=[a["href"][2:] for a in soup.find_all("div",class_="contents_1")[1].find_all("a")]
	the_number_of_elements+=len(syllabus_url_list[syllabus_list_htm[15:].split(".")[0]])

print("Exproited all urls.:")
print(syllabus_url_list)

print("creating marker files...")
for list_,value in syllabus_url_list.items():
	os.makedirs(f"./Syllabus/{list_}",exist_ok=True)
	for url in value:
		with open(f"./Syllabus/{list_}/{url}.undownloaded","w") as file:
			file.write("")

print("now,requests are about to be sent.it will take you longer than {} minutes.\
\nAfter you interrupt this process,the rest of HTMs can be downloaded with DOWNLOAD_THE_REST.py .".format(int(2*the_number_of_elements/60)))

list_count=0
the_number_of_list = len(syllabus_url_list)

for list_,value in syllabus_url_list.items():
	list_count+=1

	syllabus_count=0
	the_number_of_syllabus_in_the_list = len(value)
	for url in value:
		syllabus_count+=1
		print(f"sending query for {DATEBASES_CURRENT+url}...")
		result = requests.get(DATEBASES_CURRENT+url,timeout=(3.0,7.5))
		result.encoding = result.apparent_encoding
		print(f"{list_}/{url} was downloaded.")

		with open(f"./Syllabus/{list_}/{url}","w") as file:
			file.write(result.text)
		print(f"{list_}/{url} was written down.")
		os.remove(f"./Syllabus/{list_}/{url}.undownloaded")
		print(f"progress:{syllabus_count}/{the_number_of_syllabus_in_the_list}<-{list_count}/{the_number_of_list}")
		time.sleep(2)

input("done")