import requests
from bs4 import BeautifulSoup
import json
import time

url = "https://www.4icu.org/us/a-z/"


response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

universities = []

table = soup.find("table", {"class": "table"}) 
if table:
    rows = table.find_all("tr")[1:] 
    for i, row in enumerate(rows):
        if i >= 5: 
            break
        columns = row.find_all("td")  
        if len(columns) >= 3:
            rank = columns[0].get_text(strip=True)
            name = columns[1].get_text(strip=True)
            place = columns[2].get_text(strip=True)

            link_tag = columns[1].find("a")
            university_link = "https://www.4icu.org" + link_tag["href"] if link_tag else None

            university_details = {
                "rank": rank,
                "name": name,
                "place": place,
                "world_rank": world_rank,
                "address": address,
                "phone": phone,
                "official_website": official_website
            }

            if university_link:
                try:
                    world_rank = world_rank
                    address = address
                    phone = phone
                    official_website = official_website
                    
                
                    uni_response = requests.get(university_link, timeout=10)
                    uni_soup = BeautifulSoup(uni_response.text, "html.parser")

                    world_rank = uni_soup.find("div", {"class": "ranking"}).get_text(strip=True) if uni_soup.find("div", {"class": "ranking"}) else None
                    address = uni_soup.find("div", {"class": "address"}).get_text(strip=True) if uni_soup.find("div", {"class": "address"}) else None
                    phone = uni_soup.find("div", {"class": "phone"}).get_text(strip=True) if uni_soup.find("div", {"class": "phone"}) else None
                    official_website = uni_soup.find("a", {"class": "website"})["href"] if uni_soup.find("a", {"class": "website"}) else None

                    university_details["world_rank"] = world_rank
                    university_details["address"] = address
                    university_details["phone"] = phone
                    university_details["official_website"] = official_website

                except requests.exceptions.RequestException as e:
                    print(f"Error fetching details for {name}: {e}")

                time.sleep(1)

            universities.append(university_details)


print(json.dumps(universities, indent=2))
