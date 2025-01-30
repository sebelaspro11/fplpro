import sys
import io
import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.cinema.com.my/cinemas/cinemas.aspx"

HEADERS = {
    
    "ACCEPT": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0"
    
}
    


response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

regions = soup.find_all("div", class_="SecHeader")

# Extract the text within each a tag in the regions
text_regions = [a_tag.get_text() for region in regions for a_tag in region.find_all("a")]

# Remove 'Announcement' from the list
#filtered_values = [value for value in text_regions if value != 'Announcement']

print(text_regions)

text_regions.to_csv("test.csv")
text_regions.to_csv("./data/test.csv")
