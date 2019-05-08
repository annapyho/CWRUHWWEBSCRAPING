from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()  
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_="content_title")
    news_title = results[0].text.strip()
    results_p = soup.find_all('div', class_="article_teaser_body")
    news_p = results_p[0].text
    browser.quit()

    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results_f = soup.find_all("div", class_="carousel_container")
    for result in results_f:
        featured_image_link = result.a["data-fancybox-href"]
    featured_image_url = url.rsplit('/', 2)[0]+featured_image_link
    browser.quit()

    browser = init_browser() 
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_="js-tweet-text-container")
    weather_twit = []
    for result in results:
        weather = result.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        weather_twit.append(weather)
    mars_weather = weather_twit[0]
    browser.quit()  

    url = "https://space-facts.com/mars/"
    mars_tables = pd.read_html(url)
    mars_info = mars_tables[0]
    mars_html = mars_info.to_csv(header=None,index=False)
          
    hemisphere_image_urls = []
    hemisphere_image_urls.clear()
    hemisphere_image_urls.append({"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"})
    hemisphere_image_urls.append({"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"})
    hemisphere_image_urls.append({"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"})
    hemisphere_image_urls.append({"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"})

    mars_data = {
      "news_title": news_title,
      "news_p": news_p,
      "featured_image_url": featured_image_url,
      "mars_weather": mars_weather,
      "mars_html": mars_html,
      "hemisphere_image_urls": hemisphere_image_urls
      } 
    return mars_data