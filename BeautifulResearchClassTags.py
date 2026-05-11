import pandas
import kagglehub
import requests
from bs4 import BeautifulSoup
import time

#CSV path
path = "C:/Users/aldam/Desktop/archive/Dd5e_monsters.csv"
#get df from csv
sample = pandas.read_csv(path)
#get names column from csv as an array
sites  = sample['Name'].to_numpy()
#int for sample size


# sets up sites to loop through by appending name column to site format
for i in range(sites.size):
    sites[i] = "https://roll20.net/compendium/dnd5e/" + sites[i]

#gets beautiful soup text based on tag
def get_soup_tag(soupResponse):
    layerOne = soupResponse.find('div', class_='container primarycontentcontainer')
    layerTwoRows = layerOne.find_all('div', class_='row')
    layerTwo = layerTwoRows[2]
    layerThree = layerTwo.find('div', class_='col-md-8')
    layerFour = layerThree.find('div', class_='content-text')
    layerFive = layerFour.find('div', class_='col-md-12 attrList')
    return layerFive

#definition for getting sites
def get_site(url):
    base_response = requests.get(url)
    return BeautifulSoup(base_response.text, 'html.parser')


#definition for checking if the keyword exists for all responses
def keyword_checks(responses, keyword):
    x = 0
    for i in responses:
        if (i.find(keyword) != -1):
            x+=1
    return x

#empty array for scraped list
scraped_list = sites

#TODO,
focused_list = sites

#int for sample size
sample_size = sites.size

#loop to soup requests
start_time = time.perf_counter()

for i in range(sample_size):
    scraped_list[i] = get_site(sites[i])
    
end_time = time.perf_counter()
print(f"Elapsed time for collection: {end_time - start_time:.6f} seconds")

#loop for tag text
start_time = time.perf_counter()

for i in range(sample_size):
    focused_list[i] = get_soup_tag(scraped_list[i])
    
end_time = time.perf_counter()
print(f"Elapsed time for focused: {end_time - start_time:.6f} seconds")

runs = 5
#loop for no cleaning
start_time = time.perf_counter()

for i in range(runs):
    result = keyword_checks(scraped_list, "Points")
    
end_time = time.perf_counter()
averageOfRuns = (end_time - start_time)/runs
print(f"average: {averageOfRuns:.4f}")

print(f"Elapsed time for no clean up keyword detection: {end_time - start_time:.6f} seconds")

print(f"{result} out of {sample_size } had the keyword for uncleaned scraping")


#loop for tag keyword find time
start_time = time.perf_counter()

for i in range(runs):
    result = keyword_checks(focused_list, "Points")
    
end_time = time.perf_counter()
averageOfRuns = (end_time - start_time)/runs
print(f"average: {averageOfRuns:.4f}")

print(f"Elapsed time for focused keyword detection: {end_time - start_time:.6f} seconds")

print(f"{result} out of {sample_size } had the keyword for focused scraping")
