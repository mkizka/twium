from models import User, Status

from selenium import webdriver
from bs4 import BeautifulSoup


def tweet_parser(tweet_item: BeautifulSoup):
    try:
        text = tweet_item.find('p', class_='tweet-text').text.replace('\n', '\\n')
    except:
        return None

    user = User(
        name=tweet_item.attrs['data-name'],
        screen_name=tweet_item.attrs['data-screen-name'],
        user_id=int(tweet_item.attrs['data-user-id'])
    )
    tweet = Status(
        status_id=int(tweet_item.attrs['data-tweet-id']),
        text=text, user=user
    )
    return tweet


def driver2soup(driver: webdriver):
    return BeautifulSoup(driver.page_source, 'html.parser')
