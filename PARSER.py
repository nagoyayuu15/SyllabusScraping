from bs4 import BeautifulSoup as BS
import glob
import json
import os

os.makedirs("./SyllabusJson",exist_ok=True)

ListOfSyllabusList = glob.glob("./Syllabus/*")

count_for_list = 0
for syllabus_list in ListOfSyllabusList:
	count_for_list+=1
	folder_name=syllabus_list.split("/")[-1]
	os.makedirs(f"./SyllabusJson/{folder_name}",exist_ok=True)
	syllabuses = glob.glob(syllabus_list+"/*")
	TNO_syllabuses = len(syllabuses)

	count_for_syllabus = 0
	for syllabus in syllabuses:
		count_for_syllabus += 1
		with open(syllabus,"r") as file:
			content = file.read()
		soup = BS(content,features="lxml")
		ingredients=dict()
		for soup_ in soup.find_all("table",class_="syllabus_detail"):
			if soup_.table.tbody:
				soup_.table.tbody.unwrap()
			for soup__ in soup_.find_all("tr",recursive=False):
				soup_3 = soup__.find_all("td",recursive=False)
				if len(soup_3) != 3:
					continue
				label = soup_3[0]
				value = soup_3[2]
				ingredients[label.get_text()]=value.get_text()
		with open(
			"./SyllabusJson/{}/{}".format(folder_name,syllabus.split("/")[-1].split(".")[0]+".json"),
			"w",encoding="utf-8") as file:
			json.dump(ingredients,file,indent=2,ensure_ascii=False)
		print("progress:{}/{}<-{}/{}".format(count_for_syllabus,len(syllabuses),count_for_list,len(ListOfSyllabusList)))