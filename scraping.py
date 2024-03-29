# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Importing Pandas and Datetime
import pandas as pd
import datetime as dt

def scrape_all(): # <-- This will:
                  #     Initialize the browser.
                  #     Create a data dictionary.
                  #     End the WebDriver and return the scraped data.

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser) ## Adding code
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# *************** Title and Summary *****************
# Creating function
def mars_news(browser): 
               # ^-- this tells Python that we'll be using the 'browser'variable
               #     that was defined above. Without this, the code won't work!

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    # Adding a return statement
    return news_title, news_p

# *************** Featured Images JPL ******************

# Creating function
def featured_image(browser): 

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    #img_url

    return img_url

# ****************** Tables Mars Facts *********************

def mars_facts():

    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None
    
    # Assign columns and set index of dataframe                
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    #df
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

# ************************************************************

def hemispheres(browser):
    #executable_path = {'executable_path': ChromeDriverManager().install()}
    #browser = Browser('chrome', **executable_path, headless=True)

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    image_elem = browser.find_by_tag('a.itemLink.product-item h3')

    for i in range(len(image_elem)):
        hemisphere = {} # Initial empty dictionary

        try:
            # Find and click the image button link
            image_elem = browser.find_by_tag('a.itemLink.product-item h3')[i]
            image_elem.click()

            # Find and click the 'Sample' button
            image_sample = browser.find_by_text('Sample')[0]
            image_sample.click()
            hemisphere['image_url'] = image_sample['href'] # Adding to dictionary

            #print(hemisphere['image_url'])

            # Get the title
            hemisphere['title']=browser.find_by_css("h2.title").text # Adding to dictionary

            #print(hemisphere['title'])

            # Add data to hemisphere_image_urls list
            hemisphere_image_urls.append(hemisphere) # Adding all to dictionary

            browser.back()

        except:
            break
    
    hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())