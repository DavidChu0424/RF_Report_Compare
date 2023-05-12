import os
from os import listdir
from os.path import isfile, isdir 
import sys
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By

filepath = os.getcwd()
# file_path = os.walk(filepath)
def get_filelist(filepath):
    Filelist = []
    for home, dirs, files in os.walk(filepath):
        for filename in files:
            if "report.html" in filename:
                Filelist.append(os.path.join(home, filename))
    return Filelist
print(get_filelist(filepath))
Filelist = get_filelist(filepath)
df_table_All = pd.DataFrame()

for file in range(len(Filelist)):
    filepath = str(Filelist[file]).replace("\\","/")
    project = filepath.split("/")
    print(project[-3])
    browser = webdriver.Chrome()
    browser.get('file:///'+ filepath)

    # Total
    Telement = browser.find_element_by_xpath('//*[@id="total-stats"]')
    Ttd_content = Telement.find_elements_by_tag_name("td")
    Tlst = [] 
    for td in Ttd_content:
        Tlst.append(td.text)
    print(Tlst) 

    col = len(Telement.find_elements_by_css_selector('tr:nth-child(1) td'))
    Tlst = [Tlst[i:i + col] for i in range(0, len(Tlst), col)]


    # Data //*[@id="tag-stats"]
    element = browser.find_element_by_xpath('//*[@id="tag-stats"]')
    td_content = element.find_elements_by_tag_name("td")
    lst = [] 
    for td in td_content:
        lst.append(td.text)
    print(lst) 

    col = len(element.find_elements_by_css_selector('tr:nth-child(1) td'))
    lst = [lst[i:i + col] for i in range(0, len(lst), col)]

    Tlst.reverse()
    for j in Tlst:
        lst.insert(0, j)

    df_table = pd.DataFrame(lst)
    df_table.columns = ['Name','Total'+ str(file),'Pass'+ str(file), 'Fail'+ str(file), 'Skip'+ str(file), 'Times'+ str(file), str(project[-3])]
    df_table.set_index('Name',inplace = True)
    print(df_table)
    df_table_All = df_table_All.join(df_table, how='outer')
    print(df_table_All)
    browser.close()

df_table_All.to_excel("Report_All.xlsx")
print("Report Output Successfully !!")