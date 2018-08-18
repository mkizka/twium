import os
import json
import time
from urllib import parse

from models import User, Status

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AltApi:
    username = None
    password = None
    driver = None
    timeout = 10
    debug = False

    BASE_URL = 'https://twitter.com'
    BASE_MOBILE_URL = 'https://mobile.twitter.com'

    def __init__(self, username, password, timeout=None, debug=False):
        self.username = username
        self.password = password
        self.debug = debug
        if timeout is not None:
            self.timeout = timeout

        self._start()

    def _start(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        log_path = None
        if self.debug:
            log_path = os.path.devnull
        self.driver = webdriver.Chrome(options=options, service_log_path=log_path)

        try:
            self._load_cookies()
        except:
            pass
        if not self._is_authenticated():
            self._login()

    def _is_authenticated(self):
        self._get('/', mobile=True)
        if self.driver.current_url == self.BASE_MOBILE_URL + '/home':
            return True
        else:
            return False

    def _login(self):
        self._get('/login', mobile=True)
        self._wait(By.TAG_NAME, 'input')

        self.driver.find_element_by_name('session[username_or_email]').send_keys(self.username)
        self.driver.find_element_by_name('session[password]').send_keys(self.password)
        self._click('[data-testid="login-button"]')

        self._write_cookies()

        if self.debug and self._is_authenticated():
            print('ログイン完了')
        else:
            raise Exception('ログイン失敗')

    def _load_cookies(self):
        self._get('/', mobile=True)
        with open('cookies.json', 'r') as f:
            j = json.load(f)
        for cookie in j['cookies']:
            self.driver.add_cookie(cookie)

    def _write_cookies(self):
        cookies = self.driver.get_cookies()
        with open('cookies.json', 'w') as f:
            json.dump({'cookies': cookies}, f)

    def _get(self, path, mobile=False):
        if mobile:
            url = self.BASE_MOBILE_URL + path
        else:
            url = self.BASE_URL + path
        return self.driver.get(url)

    def _wait(self, by, value):
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def _query_selector(self, q, action):
        self.driver.execute_script(f"document.querySelector('{q}'){action}")

    def _click(self, query):
        self._query_selector(q=query, action='.click()')

    def _submit(self, query):
        self._query_selector(q=query, action='.submit()')

    def _input(self, query, value):
        self._query_selector(q=query, action=f'.value = {value}')

    def _scroll_to_bottom(self):
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def _soup(self):
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def tweet(self, text):
        search_text = parse.quote(text)
        self._get(f'/intent/tweet?text={search_text}')
        self._submit('#update-form')

    def follow(self, screen_name):
        self._get(f'/intent/follow?screen_name={screen_name}')
        self._submit('#follow_btn_form')

    def favorite(self, tweet_id):
        self._get(f'/intent/favorite?tweet_id={str(tweet_id)}')
        self._submit('#favorite_btn_form')

    def retweet(self, tweet_id):
        self._get(f'/intent/retweet?tweet_id={str(tweet_id)}')
        self._submit('#retweet_btn_form')

    def search(self, query, scroll_count=0):
        self._get(f'/search?f=tweets&q={query}')
        self._wait(By.CLASS_NAME, 'tweet-text')

        for i in range(int(scroll_count) + 1):
            self._scroll_to_bottom()
            time.sleep(1)
        soup = self._soup()

        stream_items = soup.find_all('div', class_='tweet')
        results = []
        for item in stream_items:
            try:
                text = item.find('p', class_='tweet-text').text.replace('\n', '\\n')
            except:
                break

            user = User(
                name=item.attrs['data-name'],
                screen_name=item.attrs['data-screen-name'],
                user_id=int(item.attrs['data-user-id'])
            )
            tweet = Status(
                status_id=int(item.attrs['data-tweet-id']),
                text=text, user=user
            )

            results.append(tweet)

        return results

    def __del__(self):
        self.driver.close()
