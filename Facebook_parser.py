from selenium import webdriver
import re
import time
from enum import Enum
if __name__ == "__main__":
    import sys


class Date(Enum):
    enero = 1
    febrero = 2
    marzo = 3
    abril = 4
    mayo = 5
    junio = 6
    julio = 7
    agosto = 8
    septiembre = 9
    setiembre = 9
    octubre = 10
    noviembre = 11
    diciembre = 12

    january = 1
    february = 2
    march = 3
    april = 4
    may = 5
    june = 6
    july = 7
    august = 8
    september = 9
    october = 10
    november = 11
    december = 12


class FriendInfo:

    def __init__(self, name, link_to_profile, link_to_profile_picture):
        self.name = name
        self.link_to_profile = link_to_profile
        self.link_to_profile_picture = link_to_profile_picture
        self.birthday = 0


class FacebookBot:

    user_id = 0
    friends_list = []

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.browser_connexion = webdriver.Firefox()

    def connexion(self):
        browser = self.browser_connexion
        browser.get('https://facebook.fr/')
        time.sleep(3)

        # Fill the forms
        email_form = browser.find_element_by_xpath("//input[@id='email']")
        email_form.clear()
        email_form.send_keys(self.email)

        email_form = browser.find_element_by_xpath("//input[@id='pass']")
        email_form.clear()
        email_form.send_keys(self.password)
        email_form.submit()
        time.sleep(3)

    def get_user_id(self):
        browser = self.browser_connexion

        # Get user id
        try:
            profile_button = browser.find_element_by_xpath("//div[@data-click='profile_icon']")
            profile_address = profile_button.get_attribute("innerHTML")
            print(profile_address)
            user_id = re.search('href="https:\/\/www.facebook.com\/([A-z0-9.]+)', profile_address)
            user_id = user_id.group(1)
            print("User ID is: " + user_id)
            FacebookBot.user_id = user_id
        except Exception:
            exit(1)

    def get_friend_birthday(self, link_to_profile):
        browser = self.browser_connexion
        browser.get(link_to_profile + "/about")
        time.sleep(2)

        friend_birthday_date = browser.find_element_by_xpath("//span[@class='_c24 _2ieq']")
        regex = re.search(".*?([0-9]+) de ([A-z]+) de ([0-9]+)", friend_birthday_date.text)
        birthday = str(regex.group(1)) + "/" + str(Date[regex.group(2)].value) + "/" + str(regex.group(3))
        return birthday

    def get_friends_list(self):
        browser = self.browser_connexion
        browser.get("https://www.facebook.com/" + str(FacebookBot.user_id) + "/friends?ft_ref=flsa")
        time.sleep(3)

        list_friends_list = browser.find_element_by_xpath("//ul[@class='uiList _262m _4kg']")
        list_friends_section = list_friends_list.find_elements_by_class_name("_698")

        for friend_section in list_friends_section:
            friend_info = friend_section.find_element_by_xpath(".//div[@class='fsl fwb fcb']")
            # Get friend name
            friend_name = friend_info.text
            print("Friend name: " + friend_name)

            # Get friend link to photo (Full size)
            friend_info = friend_section.find_element_by_xpath(".//a[@class='_5q6s _8o _8t lfloat _ohe']")

            print(friend_info.get_attribute("innerHTML"))
            link_to_profile_picture = re.search('src="(https://scontent-cdt1-1.xx.fbcdn.net.*?.jpg)', friend_info.get_attribute("innerHTML")).group(1)
            print("Profile picture link: " + link_to_profile_picture)

            # Get friend link to profile
            link_to_profile = re.search('(.*?)\?', friend_info.get_attribute("href")).group(1)
            print("Link to profile: " + link_to_profile + "\n")
            FacebookBot.friends_list.append(FriendInfo(friend_name, link_to_profile, link_to_profile_picture))

        for friend in FacebookBot.friends_list:
            # Get friend birthday
            birthday = self.get_friend_birthday(friend.link_to_profile)
            print(friend.name + " birthday: " + birthday)
            friend.birthday = birthday

    def close_browser(self):
        self.browser_connexion.close()


mail = sys.argv[0]
password = sys.argv[1]
mybot = FacebookBot(mail, password)
mybot.connexion()
mybot.get_user_id()
mybot.get_friends_list()

