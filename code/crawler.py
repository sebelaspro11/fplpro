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

response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")
regions = soup.find_all("div", class_="SecHeader")

# Extract text from <a> tags
text_regions = [a_tag.get_text() for region in regions for a_tag in region.find_all("a")]

# Convert list to DataFrame
df = pd.DataFrame(text_regions, columns=["Region"])

# Save to CSV
df.to_csv("test.csv", index=False)

print("CSV file has been successfully created!")
