from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
import pandas as pd
from utils.Bot_Telegram import Bot
import os


def launch_driver(url: str):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options)

    driver.get(url)
    return driver


def process_config():
    with open(os.path.join('data', 'config.json'), 'r', encoding='UTF-8') as jsonfile:
        config = json.load(jsonfile)
    return config


def login(driver, username: str, password: str):

    driver.find_element(By.ID, "session_key").send_keys(
        username)  # username

    driver.find_element(By.ID, "session_password").send_keys(
        password)  # password

    # Login
    driver.find_element(
        By.XPATH, '//*[@id="main-content"]/section[1]/div/div/form/button').click()

    # ir para pag de empregos
    driver.get("https://www.linkedin.com/jobs/")


def search(driver, job: str, location: str):
    driver.set_window_size(1080, 920)
    driver.get("https://www.linkedin.com/jobs")

    # limpar campo empregos
    driver.find_element(
        By.XPATH, '//*[contains(@id, "jobs-search-box-keyword-id")]').clear()

    # limpar campo local
    driver.find_element(
        By.XPATH, '//*[contains(@id, "jobs-search-box-location-id")]').clear()

    # preencher com o emprego
    driver.find_element(
        By.XPATH, '//*[contains(@id, "jobs-search-box-keyword-id")]').send_keys(job)

    # preencher localizacao
    driver.find_element(
        By.XPATH, '//*[contains(@id, "jobs-search-box-location-id")]').send_keys(location)

    # buscar
    driver.find_element(
        By.XPATH, '//*[@id="global-nav-search"]/div/div[2]/button[1]').click()

    time.sleep(2)

    return driver.current_url


def get_job_listings(driver):
    listings = []
    driver.set_window_size(360, 640)
    scrollHeight = 0

    for i in range(25):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        listing = soup.find_all(
            "li", {"class": "jobs-search-results__list-item"})[i]

        # scroll
        scrollHeight += 135.969
        driver.execute_script("window.scrollTo(0, " + str(scrollHeight) + ");")
        time.sleep(1)

        title = listing.find(
            "a", {"class": "job-card-list__title"}).text.strip()
        company = listing.find(
            class_="job-card-container__company-name").text.strip()
        location = listing.find(
            "li", {"class": "job-card-container__metadata-item"}).text.strip()
        link = listing.find(
            "a", {"class": "job-card-list__title"})["href"].strip()
        try:
            _easy_apply = listing.find(
                "li", {"class": "job-card-container__apply-method"}).text.strip()
            easy_apply = ("Easy Apply" in _easy_apply)
        except Exception:
            easy_apply = False
        try:
            _remote = listing.find(
                class_="job-card-container__metadata-item--workplace-type").text.strip()
            remote = "Remote" if ("Remote" in _remote) else "Not Remote"
        except Exception:
            remote = "Not Remote"
        listings.append([
            title, company, location, link])

    return listings


def get_description(driver):

    driver.set_window_size(1080, 920)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # scroll pag 1
    driver.execute_script("window.scrollTo(0, 1080);")
    see_more = driver.find_element(
        By.XPATH, "//button[@aria-label='Click to see more description']")

    driver.execute_script("arguments[0].click();", see_more)

    description = soup.find(
        "div", {"id": "job-details"}).text.strip()

    return description


def next_page(driver, i: int, search_url):
    driver.set_window_size(360, 640)
    url = search_url + "&start=" + str(i * 25)
    driver.get(url)


if __name__ == "__main__":

    driver = launch_driver("https://www.linkedin.com/")
    config = process_config()
    username = config["username"]
    password = config["password"]
    job_titles = config["job_titles"]
    locations = config["locations"]
    pages = 1

    login(driver, username, password)

    for job in job_titles:
        for location in locations:
            time.sleep(1)
            search_url = search(driver, job, location)
            try:
                for i in range(1, pages + 1, 1):
                    listings = get_job_listings(driver)
                    next_page(driver, i, search_url)
                    time.sleep(1)
            except Exception as e:
                print(e)
    driver.close()
    columns = ['VAGA', 'COMPANIA', 'LOCAL', 'LINK']
    df = pd.DataFrame(listings, columns=columns)


masterclassdsbot = Bot(token='token')
masterclassdsbot.setChatId('-IDchat')


for index, row in df.iterrows():

    masterclassdsbot.send_message(
        msg=f"Vaga: {row['VAGA']}\n" + f"Compania: {row['COMPANIA']}\n" + f"Local: {row['LOCAL']}\n" + f"Link: https://www.linkedin.com/{df['LINK'][index]}\n")
    time.sleep(0.3)
