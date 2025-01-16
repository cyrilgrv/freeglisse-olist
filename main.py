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
    id_products_list = []

    # First part of the function --> collect all URLs from the site until a page contains "No product available at the moment":
    print("Searching for all existing URLs")
    
    while not_last_page:
        url = f"{page}{page_number}"
        response = requests.get(url, headers=config.HEADERS)
        
        if "Aucun produit disponible pour le moment" in response.text:
            not_last_page = False
            print(f"First empty page found: {page_number}")
        
        else:
            url_list.append(url)
            print(f"Searched page: {page_number}, Status: {response.status_code}")
            page_number += 1

    print(f'Last page reached: {page_number-1}')

    # Second part of the function --> parsing product IDs and URLs:
    print("Starting URL and product ID search.")

    for url in url_list:
        resp = httpx.get(url)
        html = HTMLParser(resp.text)

        # Get product pages contained in a page
        products = html.css('article[data-id-product]')

        # Get URLs of product pages contained in a page
        for product in products:
            url_products_list.append(product.css_first('a[class="thumbnail product-thumbnail"]').attributes['href'])

    return url_products_list

# We run the 'get_all_urls' function for each product quality category (A, B and C):
url_products_list_A = get_all_urls(config.BASE_URLS["A"])
url_products_list_B = get_all_urls(config.BASE_URLS["B"])
url_products_list_C = get_all_urls(config.BASE_URLS["C"])

# Function to collect details of each product from the URL list of all pages on the site.
def get_details(url):
    '''
    ### Function `get_details` freeglisse.com:
    - Collects details of information for each product:
        - Product ID
        - Title
        - Price
        - Brand
        - Product characteristics: Type, User, Level, Color, CO2 savings achieved, Product type.
    #### Returns a dataframe.
    '''

    prices = []
    ids = []
    titres = []
    product_features_data_list = []
    brands = []

    for i in url:
        product_raw = requests.get(i, headers=config.HEADERS)
        details_soup = BeautifulSoup(product_raw.content)

        # Price
        try:
            price = details_soup.select_one('.current-price-value').text.strip()
        except AttributeError:
            price = None
        prices.append(price)

        # ID
        try:
            id_div = details_soup.find('div', class_='product-reference rb-tag-cate')
            id = id_div.find('span').text.strip()
        except AttributeError:
            id = None
        ids.append(id)

        # Title
        title = details_soup.find('h1').text.strip()
        titres.append(title)

        # Product characteristics: Type, User, Level, Color, CO2 savings, Product type.
        # Store all data in a dictionary (<dt> = title, <dd> = value):
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

        # Brand: if brand is not found, set to 'None' and continue
        try:
            brand = details_soup.find('img', {'class': 'img img-thumbnail manufacturer-logo'}).get('alt')
        except AttributeError:
            brand = None
        brands.append(brand)

        # Add data to a dataframe
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
for quality, url_list in zip(qualities, urls):
    df = get_details(tqdm(url_list, desc=f"Collecting products details for {quality}"))
    df["Qualité"] = quality
    dfs.append(df)
df_final = pd.concat(dfs, axis=0)
df_final.to_csv("freeglisse_export.csv", index=False)