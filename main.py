import config
import pandas as pd
import httpx
import requests
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup
from tqdm import tqdm

# Function to collect all URLs of all products on the site.
def get_all_urls(page):
    """
    ### Function `get_all_urls` freeglisse.com:
    - Collects all URLs until a page containing `No product available at the moment` is found.
    - Retrieves:
        - Product IDs of all products.
        - URLs of all product pages.
    #### Returns:
    - `url_products_list` containing URLs of all products.
    """
    
    # Define initial variables:
    page_number = 1
    not_last_page = True
    url_list = []
    url_products_list = []

    # First part of the function --> collect all URLs from the site
    print("Searching for all existing URLs")

    while not_last_page:
        url = f"{page}{page_number}"
        response = requests.get(url, headers=config.HEADERS)
        
        if "Aucun produit disponible pour le moment" in response.text:
            not_last_page = False
            print(f"First empty page found: {page_number}")
        
        else:
            url_list.append(url)
            page_number += 1
            print(f"Searched page: {page_number - 1}, Status: {response.status_code}")

    print(f'Last page reached: {page_number-1}')

    # Second part of the function --> parsing product IDs and URLs:
    print("Starting URL and product ID search.")

    for url in tqdm(url_list, desc="Parsing product pages", ncols=100):
        resp = httpx.get(url)
        html = HTMLParser(resp.text)

        # Get product pages contained in a page
        products = html.css('article[data-id-product]')

        # Get URLs of product pages contained in a page
        for product in products:
            url_products_list.append(product.css_first('a[class="thumbnail product-thumbnail"]').attributes['href'])

    return url_products_list

# We run the 'get_all_urls' function for each product quality category (A, B and C):
print("Starting URLs search for quality A")
url_products_list_A = get_all_urls(config.BASE_URLS["A"])
print("Starting URLs search for quality B")
url_products_list_B = get_all_urls(config.BASE_URLS["B"])
print("Starting URLs search for quality C")
url_products_list_C = get_all_urls(config.BASE_URLS["C"])

# Function to collect details of each product from the URL list of all pages on the site.
def get_details(url_list):
    '''
    ### Function `get_details` freeglisse.com:
    - Collects details of information for each product.
    #### Returns a dataframe.
    '''

    prices = []
    ids = []
    titres = []
    product_features_data_list = []
    brands = []

    for i in tqdm(url_list, desc="Fetching product details", ncols=100):
        product_raw = requests.get(i, headers=config.HEADERS)
        details_soup = BeautifulSoup(product_raw.content, features="html.parser")

        # Collect product data
        try:
            price = details_soup.select_one('.current-price-value').text.strip()
        except AttributeError:
            price = None
        prices.append(price)

        try:
            id_div = details_soup.find('div', class_='product-reference rb-tag-cate')
            id = id_div.find('span').text.strip()
        except AttributeError:
            id = None
        ids.append(id)

        title = details_soup.find('h1').text.strip()
        titres.append(title)

        # Collect product features
        product_features_data = {}
        product_features = details_soup.find("dl", class_="data-sheet")
        for feature in product_features.find_all(["dt", "dd"]):
            if feature.name == "dt":  # If it's a <dt>, it's a title
                title = feature.get_text(strip=True)
            elif feature.name == "dd":  # If it's a <dd>, it's a value
                value = feature.get_text(strip=True)
                if title not in product_features_data:
                    product_features_data[title] = []
                product_features_data[title].append(value)
        product_features_data_list.append(product_features_data)

        # Collect brand data
        try:
            brand = details_soup.find('img', {'class': 'img img-thumbnail manufacturer-logo'}).get('alt')
        except AttributeError:
            brand = None
        brands.append(brand)

    # Create DataFrame
    df_product = pd.DataFrame({
        "Product ID": ids,
        "Title": titres,
        "Price": prices,
        "Brand": brands
    })
    
    # Create a DataFrame with product features data
    df_product_features_data = pd.DataFrame(product_features_data_list)

    # Concatenate both dataframes ('df_product' and 'df_product_features_data')
    df = pd.concat([df_product, df_product_features_data], axis=1)

    return df

# We concatenate the dataframes for each product quality and export to a final csv
qualities = ["Qualité A", "Qualité B", "Qualité C"]
urls = [url_products_list_A, url_products_list_B, url_products_list_C]
dfs = []
for quality, url_list in zip(qualities, tqdm(urls, desc="Processing details for each quality category (A,B,C)", ncols=100)):
    df = get_details(url_list)
    df["Qualité"] = quality
    dfs.append(df)

df_final = pd.concat(dfs, axis=0)
df_final.to_csv("freeglisse_export.csv", index=False)
print("Data exported to freeglisse_export.csv")