import requests
from bs4 import BeautifulSoup
import csv
import time

# Function to scrape product listing pages and extract data


def scrape_product_listings(url, num_pages=20):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
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
            product_data["URL"] = "https://www.amazon.in" + \
                product.find("a", class_="a-link-normal").get("href")

            # Product Name
            product_data["Name"] = product.find(
                "span", class_="a-text-normal").text.strip()

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
            num_reviews = product.find(
                "span", {"class": "a-size-base", "dir": "auto"})
            if num_reviews:
                product_data["Number of reviews"] = num_reviews.text.strip()
            else:
                product_data["Number of reviews"] = "Not available"

            all_products.append(product_data)
        time.sleep(2)  # Add a small delay to avoid overwhelming the server

    return all_products

# Function to scrape individual product pages and extract more data


def scrape_product_details(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Initialize product details
    product_details = {
        "Description": "",
        "ASIN": "",
        "Product Description": "",
        "Manufacturer": ""
    }

    # ASIN
    product_details["ASIN"] = soup.find(
        "th", text="ASIN").find_next("td").text.strip()

    # Description
    product_details["Description"] = soup.find(
        "h1", {"id": "title"}).text.strip()

    # Product Description
    product_description = soup.find("div", {"id": "productDescription"})
    if product_description:
        product_details["Product Description"] = product_description.text.strip()
    else:
        product_details["Product Description"] = "Not available"

    # Manufacturer
    manufacturer = soup.find("a", {"id": "bylineInfo"})
    if manufacturer:
        product_details["Manufacturer"] = manufacturer.text.strip()
    else:
        product_details["Manufacturer"] = "Not available"

    return product_details

# Main function to orchestrate the scraping process


def main():
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    num_pages_to_scrape = 20

    # Part 1: Scrape product listing pages
    product_listings = scrape_product_listings(
        base_url, num_pages=num_pages_to_scrape)

    # Part 2: Scrape individual product pages and add more data
    data_for_export = []
    for i, product in enumerate(product_listings):
        if i >= 200:  # Limit to 200 product URLs
            break
        product_url = product["URL"]
        product_details = scrape_product_details(product_url)
        product.update(product_details)
        data_for_export.append(product)
        time.sleep(2)  # Add a small delay to avoid overwhelming the server

    # Export data to CSV file
    with open("amazon_products.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Product URL", " Product Name", "Product Price", "Rating", "Number of reviews", "Description", "ASIN",
                      "Product Description", "Manufacturer"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_for_export)

    print("Scraping and export completed successfully.")


if __name__ == "__main__":
    main()
