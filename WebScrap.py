import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio
# from openai import OpenAI

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# URL of the Times of India's Business section

# Function to extract articke heading and content
def scrape_article(url):
    # Sending a request to fetch the webpage content
    response = requests.get(url)
    
    if response.status_code == 200:
        print('response.status_code: 200',)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scraping the heading (found in <h1> -> <span>)
        print('Scraping the heading',)
        heading = soup.find('h1').find('span').text.strip()

        print('Scraping the Content',)
        content_div = soup.find('div', class_='_s30J clearfix').text.strip()
        print('Scraping the Content completed')

        return heading, content_div
    else:
        return None, "Failed to retrieve the article."
    
# Text Summerizer
def summerize_text(text):
    print("Summerizing news")
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    
    prompt = "Summarize the following text in 1-2 sentences:\n" + text
    
    response = model.generate_content(prompt)
    
    print("Summerizing news completed...")
    return response.text 




async def Scrapper():
    url = 'https://timesofindia.indiatimes.com/business'
    article_links =[]
    # Send a GET request to the URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        latest_news_section = soup.find('div', {'class': 'wRxdF'})
        # print(latest_news_section)
        if latest_news_section:
            news_items = latest_news_section.find_all('figure')
            articles=[]
            # print(news_items)
            for item in news_items:
                # Extract the full article link
                link = item.find('a')['href']
                article_links.append(link)
                # Extract article heading and content
                heading, content = scrape_article(link)
                dic = {
                    'heading':heading,
                    'content':content
                }
                # Append each article into the list
                articles.append(dic)
        else:
            print('Latest news section not found.')
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')

    #  Print the dictionary to verify
    # print(articles[:])
    print(article_links)
    summerize_articles=[]
    for i in articles:
        final_text=summerize_text(i['content'])
        summerize_articles.append(final_text)

# print(articles)
    news_dict = dict(zip(article_links,summerize_articles))
    await asyncio.sleep(1)
    return news_dict

