
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

        page.goto(BASE_URL + f"/item?page={i+1}")
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