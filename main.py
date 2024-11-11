import requests
from bs4 import BeautifulSoup
import json

url = "https://www.4icu.org/us/a-z/"

response = requests.get(url)
response.raise_for_status()  

soup = BeautifulSoup(response.text, 'html.parser')

universities = []

table = soup.find('table', {'class': 'table table-hover'})

for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')
    if len(cells) >= 3:
        rank = cells[0].text.strip()
        name = cells[1].text.strip()
        place = cells[2].text.strip()
        
    
        universities.append({
            "rank": rank,
            "name": name,
            "place": place
        })


json_data = json.dumps(universities, indent=4)

with open("universities.json", "w") as file:
    file.write(json_data)


print(json_data)
