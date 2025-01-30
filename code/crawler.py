import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Ensure 'data/' folder exists
output_folder = "data"
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

# Define the URL and Headers
url = "https://www.cinema.com.my/cinemas/cinemas.aspx"
HEADERS = {
    "ACCEPT": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0"
}

# Fetch Data
response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")
regions = soup.find_all("div", class_="SecHeader")

# Extract Text from <a> tags
text_regions = [a_tag.get_text() for region in regions for a_tag in region.find_all("a")]

# Convert List to DataFrame
df = pd.DataFrame(text_regions, columns=["Region"])

# Save CSV to 'data/' folder
csv_file_path = os.path.join(output_folder, "cinema_regions.csv")
df.to_csv(csv_file_path, index=False)

print(f"CSV file has been successfully created at {csv_file_path}!")
