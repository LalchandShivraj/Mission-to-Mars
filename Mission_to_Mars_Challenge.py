#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


#visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
#optional delay for loading the page
browser.is_element_present_by_css('div.list_test', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


#use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


#use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


#visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


#find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


#parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


#find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# In[15]:


browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# Hemispheres¶

# In[3]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser = Browser("chrome", **executable_path, headless=True)
browser.visit(url)


# In[4]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

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


# In[5]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[63]:


# 5. Quit the browser
browser.quit()


# In[ ]:




