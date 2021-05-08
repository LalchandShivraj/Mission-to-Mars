##import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import time

def scrape_all():
    #initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    #run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "new_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_image_urls(browser),
        "last_modified": dt.datetime.now()
    }

    #stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    #visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    #optional delay for loading the page
    browser.is_element_present_by_css('div.list_test', wait_time=1)

    #convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    #add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image

def featured_image(browser):
    #visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #add try/except for error handling
    try:
        #find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    #use the base url to create an absolutte url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## MARS FACTS

def mars_facts():
    #add try/except for error handling
    try:
        #read html into dataframe using read_html to scrape the facts table
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    #assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    #convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemisphere_image_urls(browser):
    # Use browser to visit the URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(1)
    # Create alist to hold the titles and images
    hemisphere_image_urls = []
    try:
        for i in range(0, 4):
            #create a dictionary to house the urls and titles (as per hint)
            hemispheres = {}
            browser.find_by_tag('h3')[i].click()
    
            #find the sample image anchor tag to get the href
            anchor = browser.find_by_text('Sample').first
    
            #add url and title to dictionary
            hemispheres['img_url'] = anchor['href']
            hemispheres['title'] = browser.find_by_tag('h2').text

            #append dictionies to list
            hemisphere_image_urls.append(hemispheres)
    
            browser.back()

    except AttributeError:
        return None
    
    return hemisphere_image_urls

#close browser
#browser.quit()

if __name__ == "__main__":
    # IF running as script, print scraped data
    print(scrape_all())
