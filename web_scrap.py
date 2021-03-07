import requests
from bs4 import BeautifulSoup
import lxml
import csv
from itertools import zip_longest

job_title=[]
company_name=[]
location_name=[]
links =[]
salary=[]
responsibilities=[]
date=[]
page_num=0
while True:
    result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}")
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    page_limit=int(soup.find("strong").text)
    if(page_num>page_limit//7):
     print("page ended,terminate")
     break
    job_titles = soup.find_all("h2", {"class": "css-m604qf"})
    company_names = soup.find_all("a", {"css-17s97q8"})
    company_locations = soup.find_all("span", {"class": "css-5wys0k"})
    posted_new = soup.find_all("div", {"class": "css-4c4ojb"})
    posted_old = soup.find_all("div", {"class": "css-do6t5g"})
    posted = [*posted_new, *posted_old]

    for i in range(len(job_titles)):
        job_title.append(job_titles[i].text)
        links.append(job_titles[i].find("a").attrs['href'])
        company_name.append(company_names[i].text)
        location_name.append(company_locations[i].text)
        date.append(posted[i].text)
    page_num+=1
    print("page switched")

for link in links:
    result = requests.get(link)
    src= result.content
    soup = BeautifulSoup(src, "lxml")
    salaries=soup.find("span",{"class":"css-8il94u"})
    #print(salaries)
    salary.append(salaries)
    requirements= soup.find("section",{"class":"css-ghicub"}).get('ul')
    respon_text=""
    for li in requirements.find_all("li"):
         respon_text+= li.text
         responsibilities.append(respon_text)



file_list=[job_title,company_name,date,location_name,links,salary,responsibilities]
exported=zip_longest(*file_list)
with open("C:/Users/Marwa/jobinfos.csv","w") as myfile:
    wr= csv.writer(myfile)
    wr.writerow(["job title","company name","date","location name","links","salary","responsibilities"])
    wr.writerows(exported)