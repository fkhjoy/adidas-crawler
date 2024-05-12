from playwright.sync_api import sync_playwright
from util import get_products_url, get_product_details, write_to_csv
# from util import get_products_url

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Use headless mode for faster execution
    product_urls = get_products_url(browser)
    data_dict_lst = []
    i = 0
    for product_url in product_urls:
        i += 1
        if i%5 == 0:
            print(f"Progress {i}/{len(product_urls)}")
        
        info = get_product_details(product_url, browser)
        if info:
            data_dict_lst.append(info)
    write_to_csv("my_data.csv", data_dict_lst)
    browser.close()