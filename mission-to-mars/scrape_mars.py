from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text.strip()
    news_p = soup.find('div', class_='article_teaser_body').text.strip()

    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)
    browser.find_by_css('.btn.btn-outline-light').click()
    featured_image_url = browser.find_by_css('.fancybox-image')['src']

    facts_url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(facts_url)
    html_table = tables[1].to_html().replace('\n', '')

    browser.visit('https://marshemispheres.com/')

    links = [link for link in browser.find_by_css('div.description a')]
    hemisphere_data = []

    for link in links:
        link.click()
        img_url = browser.links.find_by_partial_href('.tif').first['href']
        title = ' '.join(browser.find_by_css('h2.title').text.split()[:-2])
        hemisphere_data.append({'img_url': img_url, 'title': title})
        browser.back()

    mars_db = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'html_table': html_table,
        'hemisphere_data': hemisphere_data
    }

    browser.quit()

    return mars_db


# if __name__ == "__main__":
#     scraped_data = scrape()
#     print(json.dumps(scraped_data, indent=4))
