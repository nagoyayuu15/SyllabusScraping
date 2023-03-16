from bs4 import BeautifulSoup as BS
import requests
import time
import os

#CURRENT_DIRECTORY:https://syllabus.adm.nagoya-u.ac.jp/data/2023/
DATEBASES_CURRENT="https://syllabus.adm.nagoya-u.ac.jp/data/2023/"

#NOTE:list of pages which do not contain syllabus directly but secandhandaly
QUERY_FOR_SYLLABUS_LIST=["10_2023_X31000.html","10_2023_X32000.html","10_2023_X33000.html","00_2023_W1100.html","00_2023_W1200.html","00_2023_W1300.html","00_2023_W1400.html","00_2023_W1500.html","00_2023_W2100.html","00_2023_W2200.html","00_2023_W2300.html","00_2023_W3100.html","00_2023_W3200.html","00_2023_X12000.html","00_2023_X22000.html","00_2023_X90000.html"]

os.makedirs(f"./SyllabusList",exist_ok=True)

print(f"now,requests are about to be sent.it will take you longer than {len(QUERY_FOR_SYLLABUS_LIST)*2} seconds.")
for query in QUERY_FOR_SYLLABUS_LIST:
	print(f"sent query for {DATEBASES_CURRENT+query}")
	result = requests.get(DATEBASES_CURRENT+query,timeout=(3.0,7.5))
	result.encoding = result.apparent_encoding#set encoding
	print(f"{query} was downloded.")#write it down
	with open(f"./SyllabusList/{query}","w") as file:
		file.write(result.text)
	print(f"{query} was written down.")
	time.sleep(2)#buffer

input("done")