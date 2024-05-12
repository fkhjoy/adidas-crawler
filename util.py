import csv
import time

BASE_URL = "https://shop.adidas.jp"

# Scroll function with adjustable speed and delay
def slow_scroll(page, delay=1, steps=5, part=1):
    # Scroll in smaller increments to simulate a slower scroll
    scroll_height = page.evaluate("document.body.scrollHeight") * part
    step_size = scroll_height / steps

    # Scroll down in multiple steps with a delay in between
    for step in range(steps):
        page.evaluate(f"window.scrollBy(0, {step_size})")
        time.sleep(delay)  # Pause to simulate slower scroll and allow content to load

def get_products_url(browser):
    product_urls = []
    for i in range(5):
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
            # print(len(new_anchors), len(anchors))
            anchors = new_anchors
        
        # Collect all hrefs from the loaded content
        hrefs = [anchor.get_attribute('href') for anchor in anchors]
        product_urls.extend(hrefs)
        page.close()
        # for i, href in enumerate(hrefs):
        #     print(f"Anchor {i + 1} href: {href}")
    return product_urls

def get_product_details(id, browser):
    try:
        page = browser.new_page()
        page.goto(BASE_URL+id)
        print("Getting details for", id)
        info = {}
        page.wait_for_selector('body')

        # to get the reviews
        for i in range(1):
            slow_scroll(page, 0.5, 5)
        info["product_url"] = BASE_URL + id
        product_name = page.query_selector(".itemTitle").text_content()
        info["product_name"] = product_name

        
        chest = []
        back = []
        try:
            size_chart = page.query_selector_all(".sizeChartTRow span")
            headers = [item.text_content() for item in size_chart]
            per_row_count = len(headers) // 3
            for i in range(per_row_count):
                chest.append(f"{headers[i]}={headers[1*per_row_count+i]}")
                back.append(f"{headers[i]}={headers[2*per_row_count+i]}")
        except:
            pass
        info["chest_size"] = " >> ".join(chest)
        info["back_length"] = " >> ".join(back)
        
        category = page.query_selector(".categoryName").text_content()
        info["category"] = category

        price = page.query_selector(".price-value").text_content()
        info["price"] = price

        all_breadcum_category = page.query_selector_all(".breadcrumbLink")
        breadcumb_categories = [item.text_content() for item in all_breadcum_category]
        info["breadcumb_categories"] = " >> ".join(breadcumb_categories)

        all_selectable_image = page.query_selector_all(".selectableImage")
        image_urls = [BASE_URL+item.get_attribute("src") for item in all_selectable_image]
        info["image_urls"] = image_urls

        # skipping the sizes as disable
        available_sizes = page.query_selector_all(".sizeSelectorListItemButton:not(.disable)") 
        available_sizes = [item.text_content() for item in available_sizes]
        info["available_sizes"] = " >> ".join(available_sizes)

        size_sense = page.query_selector_all(".sizeFitBar .label span")
        size_sense = [item.text_content() for item in size_sense]
        info["size_sense"] = " >> ".join(size_sense)
        
        coordinate_products = []
        try:
            coordinate_products_ = page.query_selector_all(".coordinate_image")
            for item in coordinate_products_:
                img = item.query_selector("img")
                src = img.get_attribute("src")
                name = img.get_attribute("alt")
                price = item.query_selector(".coordinate_price span").text_content()
                product_number = src.split("/")[3]
                product_url = BASE_URL+f"/products/{product_number}"
                coordinate_products.append(f"name={name} ; price={price} ; number={product_number} ; image_url={src} ; product_url={product_url}")
        except:
            pass

        info["coordinated_products"] = " >> ".join(coordinate_products)

        description_title = page.query_selector(".test-commentItem-subheading").text_content()
        info["description_title"] = description_title
        general_description = page.query_selector(".commentItem-mainText").text_content()
        info["general_description"] = general_description
        description_items = page.query_selector_all(".articleFeaturesItem")
        description_items = [item.text_content() for item in description_items]
        info["description_items"] = " >> ".join(description_items)

        rating = None
        try:
            rating = page.query_selector(".BVRRNumber.BVRRRatingNumber").text_content()
            
        except:
            print("Rating not found")
            pass
        info["rating"] = rating

        review_numbers = None
        try:
            review_numbers = page.query_selector(".BVRRNumber.BVRRBuyAgainTotal").text_content()
        except:
            print("Review numbers not found")
            pass
        info["number_of_reviews"] = review_numbers

        recommended_rate = None 
        try:
            recommended_rate = page.query_selector(".BVRRBuyAgainPercentage .BVRRNumber").text_content()
        except:
            print("recommended rating not found")
        info["recommended_rate"] = recommended_rate

        sense_of_fitting = page.query_selector(".BVRRSecondaryRatingsContainer .BVRRRatingFit")
        sense_of_fitting = sense_of_fitting.query_selector("img").get_attribute("title")
        info["sense_of_fitting"] = sense_of_fitting
        appropriation_of_length = page.query_selector(".BVRRSecondaryRatingsContainer .BVRRRatingLength")
        appropriation_of_length = appropriation_of_length.query_selector("img").get_attribute("title")
        info["appropriation_of_length"] = appropriation_of_length
        quality_of_material = page.query_selector(".BVRRSecondaryRatingsContainer .BVRRRatingQuality")
        quality_of_material = quality_of_material.query_selector("img").get_attribute("title")
        info["quality_of_material"] = quality_of_material
        comfort = page.query_selector(".BVRRSecondaryRatingsContainer .BVRRRatingComfort")
        comfort = comfort.query_selector("img").get_attribute("title")
        info["comfort"] = comfort

        user_reviews = []
        try:
            user_reviews_ = page.query_selector_all(".BVRRContentReview")
            for user_review in user_reviews_:
                try:
                    reviewer_id = user_review.query_selector(".BVRRNickname").text_content()
                    date = user_review.query_selector(".BVRRReviewDate").text_content()
                    rating = user_review.query_selector(".BVRRRating").query_selector("img").get_attribute("title")
                    title = user_review.query_selector(".BVRRReviewTitle").text_content()
                    description = user_review.query_selector(".BVRRReviewTextParagraph").text_content()
                    data = f"date={date} ; rating={rating} ; title={title} ; description={description} ; reviewer_id={reviewer_id}"
                    user_reviews.append(data)
                except:
                    pass
        except:
            pass
        info["user_reviews"] = " >> ".join(user_reviews)
        
        kws = page.query_selector_all("div.test-category_link a")
        kws = [item.text_content() for item in kws]
        info["kws"] = " >> ".join(kws)
        
        page.close()
        return info
    except:
        page.close()
        return False

def write_to_csv(file_name, data_dict_lst):
    try:
        with open(file_name, "w") as f:
            w = csv.DictWriter(f, data_dict_lst[0].keys())
            w.writeheader()
            for data in data_dict_lst:
                w.writerow(data)
    except Exception as e:
        print(e)