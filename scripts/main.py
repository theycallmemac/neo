#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv, exit
from os import environ
from tempfile import NamedTemporaryFile
from subprocess import call
from time import sleep
from click import command, echo, argument
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def get_credentials():
    fb_email, fb_pw = input("Facebook Login Email: "), getpass(
        "Facebook Password: ")
    return [fb_email, fb_pw]


def open_vim():
    title = input("Event Name: ")
    with NamedTemporaryFile(suffix='tmp') as tmp:
        call(['vim', tmp.name])
        description = open(tmp.name, 'r').read()
        return [title, description]


def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-notifications")
    ffprofile = webdriver.FirefoxProfile()
    ffprofile.set_preference("dom.webnotifications.enabled", False)
    driver = webdriver.Firefox(firefox_profile=ffprofile,
                               firefox_options=options, executable_path='/usr/local/bin/geckodriver')
    return driver


def fb_login(fb, event_description, details):
    driver = setup_driver()
    driver.get('https://www.facebook.com/login/')
    email = driver.find_element_by_name('email')
    pw = driver.find_element_by_name('pass')
    login = driver.find_element_by_name('login')
    email.send_keys(fb[0])
    pw.send_keys(fb[1])
    login.click()
    fb_create(driver, event_description, details)


def fb_create(driver, event_description, details):
    driver.get('https://www.facebook.com/dcuredbrick/')
    event = driver.find_elements(
        By.XPATH, '//span[text()="Create an event"]')[0]
    driver.execute_script("window.scrollTo(0, 1000)")
    event.click()
    sleep(15)
    event_name, location, description = driver.find_element(
        By.XPATH, "//input[@data-testid='event-create-dialog-name-field']"), driver.find_element(
        By.XPATH, "//input[@data-testid='event-create-dialog-where-field']"), driver.find_element(
        By.XPATH, "//div[@data-testid='event-create-dialog-details-field']")

    start_hour, start_min, start_ampm, start_date = driver.find_elements_by_class_name('_4nx3')[0], driver.find_elements_by_class_name(
        '_4nx3')[1], driver.find_elements_by_class_name('_4nx3')[2], driver.find_elements(By.XPATH, "//input[@placeholder='mm/dd/yyyy']")[0]
    end_hour, end_min, end_ampm, end_date = driver.find_elements_by_class_name('_4nx3')[3], driver.find_elements_by_class_name(
        '_4nx3')[4], driver.find_elements_by_class_name('_4nx3')[5], driver.find_elements(By.XPATH, "//input[@placeholder='mm/dd/yyyy']")[1]

    event_name.send_keys(event_description[0])
    location.send_keys(details[0])
    description.send_keys(event_description[1])

    driver.execute_script(f"arguments[0].value = '{details[3]}';", start_date)
    begin_hr, begin_min = int(details[1][:2]), str(details[1][3:])
    ampm = get_am_or_pm(begin_hr)
    begin_hr = str(begin_hr)
    driver.execute_script(
        f'arguments[0].innerHTML = "{begin_hr}";', start_hour)
    driver.execute_script(
        f'arguments[0].innerHTML = "{begin_min}";', start_min)
    driver.execute_script(
        f'arguments[0].innerHTML = "{ampm}";', start_ampm)

    driver.execute_script(f"arguments[0].value = '{details[3]}';", end_date)
    finish_hr, finish_min = int(details[2][:2]), str(details[2][3:])
    ampm = get_am_or_pm(finish_hr)
    finish_hr = str(finish_hr)
    driver.execute_script(
        f'arguments[0].innerHTML = "{finish_hr}";', end_hour)
    driver.execute_script(
        f'arguments[0].innerHTML = "{finish_min}";', end_min)
    driver.execute_script(
        f'arguments[0].innerHTML = "{ampm}";', end_ampm)
    submit = driver.find_element(
        By.XPATH, "//button[@data-testid='event-create-dialog-confirm-button']")
    submit.click()
    driver.quit()


def get_am_or_pm(time):
    if time > 11:
        time = time - 12
        ampm = 'PM'
    else:
        time = time,
        ampm = 'AM'

    return ampm


@command()
@argument('room')
@argument('start_time')
@argument('end_time')
@argument('date')
def cli(room, start_time, end_time, date):
    details = [room, start_time, end_time, date]
    facebook = get_credentials()
    event_description = open_vim()
    fb_login(facebook, event_description, details)
