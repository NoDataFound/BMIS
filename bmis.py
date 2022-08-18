#python3 -m pip install profanity-check
#python3 -m pip install alt-profanity-check
#python3 -m pip install joblib
#python3 -m pip install sklearn
#python3 -m pip install selenium
#python3 -m pip install webdriver-manager
#python3 -m pip install scipy
# you might need to pip3 uninstall scipy and re-install
#adapted from https://github.com/jaymark22/TwitterWebScraper 
#https://chromedriver.storage.googleapis.com/index.html?path=104.0.5112.79/

import sys
import time
import re
import csv
from getpass import getpass
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from profanity_check import predict, predict_prob
import pandas as pd



print('''

   [0] =               ✴.·´¯`·.·★  🎀𝓵𝓲𝓽𝓽𝓵𝓮 𝓶𝓪𝓭🎀  ★·.·`¯´·.✴ 
|======== ======== ======== ======== ======== ======== ======== ======== ========|   
   
   [1] =    /$$$$$$$  /$$$$$$  /$$$$$$        /$$      /$$  /$$$$$$  /$$$$$$$ 
           | $$__  $$|_  $$_/ /$$__  $$      | $$$    /$$$ /$$__  $$| $$__  $$
           | $$  \ $$  | $$  | $$  \__/      | $$$$  /$$$$| $$  \ $$| $$  \ $$
           | $$$$$$$   | $$  | $$ /$$$$      | $$ $$/$$ $$| $$$$$$$$| $$  | $$
           | $$__  $$  | $$  | $$|_  $$      | $$  $$$| $$| $$__  $$| $$  | $$
           | $$  \ $$  | $$  | $$  \ $$      | $$\  $ | $$| $$  | $$| $$  | $$
           | $$$$$$$/ /$$$$$$|  $$$$$$/      | $$ \/  | $$| $$  | $$| $$$$$$$/
           |_______/ |______/ \______/       |__/     |__/|__/  |__/|_______/ 
                                                              
''')
print('Locating Browser...')
time.sleep(0.5)
print('Initializing Twitter...')
time.sleep(0.3)
print('Log in... its safe. I promise.')
time.sleep(0.3)
for i in range(0, 80, 1):
    print("░", end="")
    sys.stdout.flush()
    time.sleep(0.01)
print(" ")
 
options = Options()
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.twitter.com/login')
driver.maximize_window()
subject = "Infosec"

sleep(35)
#Giving you time for 2FA

search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
search_box.send_keys(subject)
search_box.send_keys(Keys.ENTER)

sleep(3)
latest = driver.find_element(By.XPATH,
                             '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div')

latest.click()
sleep(3)
Usernames = []
TimeStamps = []
Tweets = []
Replies = []
Retweets = []
Likes = []

articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
while True:
    for article in articles:
        Username = driver.find_element(By.XPATH, ".//div[@data-testid='User-Names']").text
        TimeStamp = driver.find_element(By.XPATH, ".//time").get_attribute('datetime')
        Tweet = driver.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
        Reply = driver.find_element(By.XPATH, ".//div[@data-testid='reply']").text
        Retweet = driver.find_element(By.XPATH, ".//div[@data-testid='retweet']").text
        Like = driver.find_element(By.XPATH, "//div[@data-testid='like']").text

        if Username not in Usernames:
            Usernames.append(Username)
            TimeStamps.append(TimeStamp)
            Tweets.append(Tweet)
            Replies.append(Reply)
            Retweets.append(Retweet)
            Likes.append(Like)

    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(3)
    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    Tweets2 = list(set(Tweets))
    if len(Tweets2) > 100:
        break

dataframe = {'UserName': Usernames, 'TimeStamps': TimeStamps, 'Tweets': Tweets, 'Replies': Replies, 'Retweets': Retweets, 'Likes': Likes,}
df = pd.DataFrame(dataframe)
df.to_csv('InfoSec.csv')
data = pd.read_csv('InfoSec.csv')
tweets = data['Tweets'].astype(str)
print("|======== ======== ======== ======== RESULTS ======== ======== ======== ========|" )
for tweet in tweets:
    print(predict([tweet]),","+tweet)
