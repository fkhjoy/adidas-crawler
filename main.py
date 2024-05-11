from playwright.sync_api import sync_playwright
import time
# from util import get_products_url

BASE_URL = "https://shop.adidas.jp"

# Scroll function with adjustable speed and delay
def slow_scroll(page, delay=1, steps=5):
    # Scroll in smaller increments to simulate a slower scroll
    scroll_height = page.evaluate("document.body.scrollHeight")
    step_size = scroll_height / steps

    # Scroll down in multiple steps with a delay in between
    for step in range(steps):
        page.evaluate(f"window.scrollBy(0, {step_size});")
        time.sleep(delay)  # Pause to simulate slower scroll and allow content to load

def get_products_url(browser):
    product_urls = []
    for i in range(1):
        page = browser.new_page()

        page.goto(BASE_URL + f"/item?page={i+1}&category=wear", timeout=50000)
        anchors = []
        # Simulate scrolling to the bottom to load more content
        while True:
            # Scroll to the bottom of the page
            slow_scroll(page, .5, 5)

            # Check if more content has been loaded
            new_anchors = page.query_selector_all('.image_link')
            
            # Break if no new content is loaded
            if len(new_anchors) == len(anchors):
                break
            print(len(new_anchors), len(anchors))
            anchors = new_anchors
        
        # Collect all hrefs from the loaded content
        hrefs = [anchor.get_attribute('href') for anchor in anchors]
        product_urls.extend(hrefs)
        page.close()
        # for i, href in enumerate(hrefs):
        #     print(f"Anchor {i + 1} href: {href}")
    return product_urls

def get_product_details(id, browser):
    page = browser.new_page()
    page.goto(BASE_URL+id)
    info = {}
    page.wait_for_selector('body')
    # to get the reviews
    for i in range(1):
        slow_scroll(page, 1)

    product_name = page.query_selector(".itemTitle").text_content()
    info["product_name"] = product_name

    category = page.query_selector(".categoryName").text_content()
    info["category"] = category

    price = page.query_selector(".price-value").text_content()
    info["price"] = price

    all_breadcum_category = page.query_selector_all(".breadcrumbLink")
    breadcumb_categories = [item.text_content() for item in all_breadcum_category]
    info["breadcumb_categories"] = breadcumb_categories

    # all_selectable_image = page.query_selector_all(".selectableImage")
    # image_urls = [BASE_URL+item.get_attribute("src") for item in all_selectable_image]
    # info["image_urls"] = image_urls

    # skipping the sizes as disable
    available_sizes = page.query_selector_all(".sizeSelectorListItemButton:not(.disable)") 
    available_sizes = [item.text_content() for item in available_sizes]
    info["available_sizes"] = available_sizes

    size_sense = page.query_selector_all(".sizeFitBar .label span")
    size_sense = [item.text_content() for item in size_sense]
    info["size_sense"] = size_sense

    # coordinate_products = page.query_selector_all(".coordinate_image")
    # coordinate_products = [(item.get_attribute("src"), item.get_attribute("alt")) for item in coordinate_products]
    # info["coordinate_products"] = coordinate_products

    description_title = page.query_selector(".test-commentItem-subheading").text_content()
    info["description_title"] = description_title
    general_description = page.query_selector(".commentItem-mainText").text_content()
    info["general_description"] = general_description
    description_items = page.query_selector_all(".articleFeaturesItem")
    description_items = [item.text_content() for item in description_items]
    info["description_items"] = description_items

    for i in range(1):
        slow_scroll(page, .5)
    rating = page.query_selector(".BVRRNumber.BVRRRatingNumber").text_content()
    info["rating"] = rating
    review_numbers = page.query_selector(".BVRRNumber.BVRRBuyAgainTotal").text_content()
    info["number_of_reviews"] = review_numbers
    recommended_rate = page.query_selector(".BVRRBuyAgainPercentage .BVRRNumber").text_content()
    info["recommended_rate"] = recommended_rate

    kws = page.query_selector_all("div.test-category_link a")
    kws = [item.text_content() for item in kws]
    info["kws"] = kws

    return info   


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Use headless mode for faster execution
    # product_urls = get_products_url(browser)
    
        # for i, href in enumerate(hrefs):
        #     print(f"Anchor {i + 1} href: {href}")
    # print(len(product_urls))
    # print(product_urls[1])
    product_url = "/products/IX6438"
    info = get_product_details(product_url, browser)
    print("info@@@@@@@@@@@@\n")
    for key, value in info.items():
        print(key,"--->", value)
    
    browser.close()