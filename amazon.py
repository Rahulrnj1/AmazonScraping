
import requests
from bs4 import BeautifulSoup
import csv
import time

# Function to scrape product listing pages and extract data
def scrape_product_listings(url, num_pages=20):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    all_products = []

    for page in range(1, num_pages + 1):
        print(f"Scraping page {page}...")
        page_url = url + f"&page={page}"
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("div", class_="s-include-content-margin")

        for product in products:
            product_data = {}

            # Product URL
            product_data["URL"] = "https://www.amazon.in" + product.find("a", class_="a-link-normal").get("href")

            # Product Name
            product_data["Name"] = product.find("span", class_="a-text-normal").text.strip()

            # Product Price
            price = product.find("span", class_="a-offscreen")
            if price:
                product_data["Price"] = price.text.strip()
            else:
                product_data["Price"] = "Not available"

            # Rating
            rating = product.find("span", class_="a-icon-alt")
            if rating:
                product_data["Rating"] = rating.text.split()[0]
            else:
                product_data["Rating"] = "Not available"

            # Number of reviews
            num_reviews = product.find("span", {"class": "a-size-base", "dir": "auto"})
            if num_reviews:
                product_data["Number of reviews"] = num_reviews.text.strip()
            else:
                product_data["Number of reviews"] = "Not available"

            all_products.append(product_data)
        time.sleep(2)  # Add a small delay to avoid overwhelming the server

    return all_products

# Function to export data to CSV file
def export_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Product URL", "Product Name", "Product Price", "Rating", "Number of reviews"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Main function for Part 1
def part1_main():
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    num_pages_to_scrape = 20

    # Part 1: Scrape product listing pages
    product_listings = scrape_product_listings(base_url, num_pages=num_pages_to_scrape)

    # Export data to CSV file
    export_to_csv(product_listings, "amazon_products_part1.csv")

    print("Scraping and export for Part 1 completed successfully.")

if __name__ == "__main__":
    part1_main()
