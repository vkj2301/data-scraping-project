import openpyxl
from bs4 import BeautifulSoup
import requests

# Function to extract product details from a single page
def extract_product_details(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    product_divs = soup.find_all('div', class_='s-card-container')

    products_data = []
    for div in product_divs:
        product_name = div.find('span', class_='a-size-medium')
        product_name = product_name.text.strip() if product_name else " "

        product_price = div.find('span', class_='a-price-whole')
        product_price = product_price.text.strip() if product_price else " "

        product_review = div.find('span', class_='a-size-base s-underline-text')
        product_review = product_review.text.strip() if product_review else " "

        product_rating = div.find('span', class_='a-icon-alt')
        product_rating = product_rating.text.strip().split()[0] if product_rating else " "

        products_data.append([product_name, product_price, product_review, product_rating])

    return products_data

# Main function to process multiple pages and save data to Excel
def scrape_amazon_bags():
    excel_file = openpyxl.Workbook()
    sheet = excel_file.active
    sheet.append(['Product Name', 'Product Price', 'Product Review', 'Product Rating'])

    base_url = "https://www.amazon.in/s?k=bags&page="

    for page_num in range(1, 21):  # Scrape 20 pages
        url = base_url + str(page_num)
        response = requests.get(url)
        if response.status_code == 200:
            products_data = extract_product_details(response.content)
            for product_data in products_data:
                sheet.append(product_data)

    excel_file.save('amazon_bags_data.csv')

if __name__ == "__main__":
    scrape_amazon_bags()
