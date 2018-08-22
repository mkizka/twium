from models import User, Status, Notify

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


def activity_parser(activity_item: BeautifulSoup):
    user_items = activity_item.find_all('a', class_='js-profile-popup-actionable')
    users = []
    for user_item in user_items:
        s = User(
            name=user_item.attrs['title'],
            screen_name=user_item.attrs['href'][1:],
            user_id=int(user_item.attrs['data-user-id'])
        )
        users.append(s)

    tweet_item = activity_item.find('div', class_='QuoteTweet-innerContainer')
    tweet_user = User(
        name=tweet_item.find('b', class_='QuoteTweet-fullname').text,
        screen_name=tweet_item.attrs['data-screen-name'],
        user_id=int(tweet_item.attrs['data-user-id'])
    )
    tweet = Status(
        text=tweet_item.find('div', class_='QuoteTweet-text').text,
        status_id=int(tweet_item.attrs['data-item-id']),
        user=tweet_user
    )

    notify = Notify(
        activity_type=activity_item.attrs['data-component-context'],
        users=users,
        tweet=tweet
    )
    return notify


def driver2soup(driver: webdriver):
    return BeautifulSoup(driver.page_source, 'html.parser')
