import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the website to scrape
url = "http://books.toscrape.com/"

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the container with the list of books
    books_container = soup.find_all('article', class_='product_pod')
    
    # Create lists to store the data
    titles = []
    prices = []
    availability = []

    # Loop through the container and extract data
    for book in books_container:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        availability_status = book.find('p', class_='instock availability').text.strip()
        
        titles.append(title)
        prices.append(price)
        availability.append(availability_status)

    # Create a DataFrame using pandas
    books_df = pd.DataFrame({
        'Title': titles,
        'Price': prices,
        'Availability': availability
    })
    
    # Save the DataFrame to a CSV file
    books_df.to_csv('books.csv', index=False)
    
    print("Data has been successfully scraped and saved to books.csv")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
