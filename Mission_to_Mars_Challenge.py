# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Importing Pandas
import pandas as pd

# Setting executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
#YN = True
YN = False
browser = Browser('chrome', **executable_path, headless=YN)

# ### Title and Summary

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images

# Run block of code before "Title and Summary"

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ### Tables

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()

#browser.quit()

# ### Hemispheres

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

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()



