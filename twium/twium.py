import json
import math
import os
import re
import time
from typing import Union, Callable
from urllib import parse

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from twium.models import Tweet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_SEARCH_COUNT = 200
AUTHORIZATION = 'Bearer ' \
                'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4pu' \
                'Ts%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
     'AppleWebKit/537.36 (KHTML, like Gecko) ' \
     'Chrome/78.0.3904.108 Safari/537.36'


class AltApi:
    is_authenticated = False
    session: requests.Session = None

    BASE_URL = 'https://twitter.com'
    BASE_MOBILE_URL = 'https://mobile.twitter.com'

    def __init__(self, timeout: int = 10, debug: bool = False, driver: WebDriver = None):
        self.debug = debug
        self.timeout = timeout

        if driver is None:
            self.driver = self._create_driver()
        else:
            self.driver = driver

    def _create_driver(self) -> WebDriver:
        options = webdriver.ChromeOptions()
        if not self.debug:
            options.add_argument('--headless')

        log_path = None
        if not self.debug:
            log_path = os.path.devnull

        return webdriver.Chrome(options=options, service_log_path=log_path)

    def _is_authenticated(self) -> bool:
        self._get('/', mobile=True)

        try:
            self._wait(lambda x: self.driver.current_url == self.BASE_MOBILE_URL + '/home')
            self.is_authenticated = True
        except:
            self.is_authenticated = False

        self.session = self._get_session()
        return self.is_authenticated

    def auth(self, username: str, password: str):
        self._get('/login', mobile=True)
        self._wait((By.NAME, 'session[username_or_email]'))

        self.driver.find_element_by_name('session[username_or_email]').send_keys(username)
        self.driver.find_element_by_name('session[password]').send_keys(password)
        self._click('[data-testid=LoginForm_Login_Button]')

        if not self._is_authenticated():
            raise Exception('ログイン失敗')

    def load_cookies(self, filepath: str):
        self._get('/', mobile=True)

        with open(filepath, 'r') as f:
            j = json.load(f)
        for cookie in j['cookies']:
            # Seleniumの実装の都合上expiryの形式が異なる
            if 'expiry' in cookie.keys():
                cookie['expiry'] = int(cookie['expiry'])
            self.driver.add_cookie(cookie)

        if not self._is_authenticated():
            raise Exception('ログイン失敗')

    def write_cookies(self, filepath: str):
        cookies = self.driver.get_cookies()
        with open(filepath, 'w') as f:
            json.dump({'cookies': cookies}, f)

    def _get(self, path: str, mobile=False):
        if mobile:
            url = self.BASE_MOBILE_URL + path
        else:
            url = self.BASE_URL + path
        return self.driver.get(url)

    def _wait(self, condition: Union[tuple, Callable]):
        if type(condition) is tuple:
            condition = EC.visibility_of_element_located(condition)
        WebDriverWait(self.driver, self.timeout).until(condition)

    def _query_selector(self, q: str, action: str):
        self._wait((By.CSS_SELECTOR, q))
        self.driver.execute_script(f"document.querySelector('{q}'){action}")

    def _click(self, query: str):
        self._query_selector(q=query, action='.click()')

    def _submit(self, query: str):
        self._query_selector(q=query, action='.submit()')

    def _input(self, query: str, value: str):
        self._query_selector(q=query, action=f'.value = {value}')

    def _get_session(self) -> requests.Session:
        session = requests.Session()
        for cookie in self.driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        csrf_token = requests.utils.dict_from_cookiejar(session.cookies)['ct0']
        session.headers.update({
            'Authorization': AUTHORIZATION,
            'User-Agent': UA,
            'X-Twitter-Auth-Type': 'OAuth2Session',
            'X-Twitter-Active-User': 'yes',
            'Origin': 'https://twitter.com',
            'X-CSRF-Token': csrf_token,
        })
        return session

    def tweet(self, text: str, in_reply_to_status_id=None) -> int:
        tweet_text = parse.quote(text)
        url = f'/intent/tweet?text={tweet_text}'
        if in_reply_to_status_id is not None:
            url += f'&in_reply_to_status_id={str(in_reply_to_status_id)}'
        self._get(url)
        self._submit('#update-form')
        # ツイートされたIDを返す
        return int(re.findall(r'[0-9]+$', self.driver.current_url)[0])

    def del_tweet(self, tweet_id: int):
        response = self.session.post(
            'https://api.twitter.com/1.1/statuses/destroy.json',
            {'tweet_mode': 'extended', 'id': tweet_id}
        )
        response.raise_for_status()

    def _get_user_intent(self, user_id: int = None, screen_name: str = None):
        url = '/intent/user?'
        if user_id:
            url += f'user_id={str(user_id)}'
        elif screen_name:
            url += f'screen_name={screen_name}'
        else:
            return
        self._get(url)

    def follow(self, user_id: int = None, screen_name: str = None):
        self._get_user_intent(user_id, screen_name)
        self._submit('form.follow')

    def unfollow(self, user_id: int = None, screen_name: str = None):
        self._get_user_intent(user_id, screen_name)
        self._submit('form.unfollow')

    def favorite(self, tweet_id: int):
        self._get(f'/intent/favorite?tweet_id={str(tweet_id)}')
        self._submit('#favorite_btn_form')

    def retweet(self, tweet_id: int):
        self._get(f'/intent/retweet?tweet_id={str(tweet_id)}')
        self._submit('#retweet_btn_form')

    def search(self, word: str, count: int = MAX_SEARCH_COUNT):
        result = []
        cursor = ''
        for i in range(math.ceil(count / MAX_SEARCH_COUNT)):
            url = 'https://api.twitter.com/2/search/adaptive.json?'
            url += parse.urlencode({
                'tweet_search_mode': 'live',
                'cursor': cursor,
                'include_profile_interstitial_type': 1,
                'include_blocking': 1,
                'include_blocked_by': 1,
                'include_followed_by': 1,
                'include_want_retweets': 1,
                'include_mute_edge': 1,
                'include_can_dm': 1,
                'include_can_media_tag': 1,
                'skip_status': 1,
                'cards_platform': 'Web-12',
                'include_cards': 1,
                'include_composer_source': 'true',
                'include_ext_alt_text': 'true',
                'include_reply_count': 1,
                'tweet_mode': 'extended',
                'include_entities': 'true',
                'include_user_entities': 'true',
                'include_ext_media_color': 'true',
                'include_ext_media_availability': 'true',
                'send_error_codes': 'true',
                'simple_quoted_tweets': 'true',
                'q': word,
                'count': count if count < MAX_SEARCH_COUNT else MAX_SEARCH_COUNT,
                'query_source': 'typed_query',
                'pc': 1,
                'spelling_corrections': 1,
                'ext': 'mediaStats, highlightedLabel, cameraMoment',
            })
            response = self.session.get(url)
            response.raise_for_status()
            response_json = json.loads(response.text)

            last_timeline_content = response_json['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']
            if 'operation' in last_timeline_content.keys():
                cursor = last_timeline_content['operation']['cursor']['value']

            count -= MAX_SEARCH_COUNT
            result += list(map(lambda j: Tweet(j), response_json['globalObjects']['tweets'].values()))

            time.sleep(1)
        return sorted(result, key=lambda tweet: tweet.created_at, reverse=True)

    def __del__(self):
        self.driver.close()
