#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv, exit
from os import environ
from tempfile import NamedTemporaryFile
from subprocess import call
from click import command, echo, argument
from getpass import getpass
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from concurrent.futures import ThreadPoolExecutor
import smtplib


def get_fb_credentials():
    fb_email, fb_pw = input("Facebook Login Email: "), getpass(
        "Facebook Password: ")
    return [fb_email, fb_pw]


def get_goog_credentials():
    goog_email, dcu_uname, dcu_pw = input("Gmail: "), input(
        "DCU Username: "), getpass("DCU Password: ")
    return [goog_email, dcu_uname, dcu_pw]


def event_setup():
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
    driver = webdriver.Firefox(
        firefox_profile=ffprofile,
        firefox_options=options,
        executable_path='/usr/local/bin/geckodriver')
    return driver


def fb_login(fb, event_description, details):
    driver = setup_driver()
    driver.get('https://www.facebook.com/login/')
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    email = driver.find_element_by_name('email')
    pw = driver.find_element_by_name('pass')
    login = driver.find_element_by_name('login')
    email.send_keys(fb[0])
    pw.send_keys(fb[1])
    login.click()
    fb_create(driver, event_description, details)


def fb_create(driver, event_description, details):
    driver.get('https://www.facebook.com/dcuredbrick/')
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, '//span[text()="Create an event"]'))
    )
    event = driver.find_elements(
        By.XPATH, '//span[text()="Create an event"]')[0]
    driver.execute_script("window.scrollTo(0, 1000)")
    event.click()
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@data-testid='event-create-dialog-name-field']"))
    )
    event_name, location, description = driver.find_element(
        By.XPATH, "//input[@data-testid='event-create-dialog-name-field']"), driver.find_element(
        By.XPATH, "//input[@data-testid='event-create-dialog-where-field']"), driver.find_element(
        By.XPATH, "//div[@data-testid='event-create-dialog-details-field']")

    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, '_4nx3'))
    )
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


def goog_login(google, event_description, details):
    driver = setup_driver()
    driver.get('https://accounts.google.com/ServiceLogin')

    email = driver.find_element_by_id('identifierId')
    next = driver.find_element_by_id('identifierNext')
    email.send_keys(google[0])
    next.click()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    uname = driver.find_element_by_id('username')
    pw = driver.find_element_by_id('password')
    uname.send_keys(google[1])
    pw.send_keys(google[2])
    proceed = driver.find_element_by_name('_eventId_proceed')
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "_eventId_proceed"))
    )
    proceed.click()
    cal_create(driver, event_description, details, google)


def cal_create(driver, event_description, details, google):
    driver.get('https://calendar.google.com/calendar/r/')

    email = driver.find_element_by_id('identifierId')
    next = driver.find_element_by_id('identifierNext')
    email.send_keys(google[0])
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "identifierNext"))
    )
    next.click()
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "zlaSJd"))
    )
    plus = driver.find_element_by_class_name('zlaSJd')
    plus.click()
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "xTiIn"))
    )
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "hInySc0"))
    )
    event_name, location, description = driver.find_element_by_id(
        'xTiIn'), driver.find_elements_by_class_name('whsOnd')[5], driver.find_element_by_id('hInySc0')
    event_name.send_keys(event_description[0])
    location.send_keys(details[0])
    description.send_keys(event_description[1])
    start_time, start_date = driver.find_element_by_id(
        'xStTiIn'), driver.find_element_by_id('xStDaIn')
    break_date = details[3].split("/")
    formatted_date = ''.join(
        [break_date[0], break_date[1], break_date[2]])
    dates = driver.find_elements_by_class_name('r4nke')[1:]
    start_date.click()
    for date in dates:
        if break_date[0] == date.text:
            date.click()
    time = int(details[1][:2])
    ampm = get_am_or_pm(time).lower()
    details[1] += ampm
    driver.execute_script(
        f"arguments[0].value = '{details[1]}';", start_time)
    end_time, end_date = driver.find_element_by_id(
        'xEnTiIn'), driver.find_element_by_id('xEnDaIn')
    end_date.click()
    for date in dates:
        if break_date[0] == date.text:
            date.click()
    time = int(details[2][:2])
    ampm = get_am_or_pm(time).lower()
    details[2] += ampm
    driver.execute_script(
        f"arguments[0].value = '{details[2]}';", end_time)
    calendar = driver.find_elements_by_class_name('Z7IIl')[0]
    calendar.click()
    cals = driver.find_elements_by_class_name('Z7IIl')
    for cal in cals:
        if cal.text == "Redbrick DCU's Networking Society":
            cal.click()
            break
    save = driver.find_elements_by_class_name('RveJvd')[6]
    save.click()
    driver.quit()


def book_lab(goog, details):
    FROM = goog[0]
    TO = ['james.mcdermott89@gmail.com']
    SUBJECT = 'Lab Booking'
    BODY = "Just wondering if you could book " + \
        details[0] + " on the " + \
        details[3] + " from " + details[1] + " to " + details[2] + \
        " for Redbrick" + ".\n\nThank you."
    message = """\nFrom: %s\nTo: %s\nSubject: %s\n\n%s""" % (
        FROM, ", ".join(TO), SUBJECT, BODY)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(goog[0], goog[2])
    server.sendmail(FROM, TO, message)
    server.close()


def facebook_operations(fb, event_description, details):
    fb_login(fb, event_description, details)
    return "Created Facebook Event."


def google_operations(goog, event_description, details):
    goog_login(goog, event_description, details)
    return "Created Calendar Event."


def email_operations(goog, event_description, details):
    book_lab(goog, details)
    return "Booked Room."


@command()
@argument('room')
@argument('start_time')
@argument('end_time')
@argument('date')
def cli(room, start_time, end_time, date):
    details = [room, start_time, end_time, date]
    executors = []
    event_description = event_setup()
    echo(f"Event Description: {event_description[1]}")
    google = get_goog_credentials()
    facebook = get_fb_credentials()
    with ThreadPoolExecutor(max_workers=8) as executor:
        # executors.append(executor.submit(
        #    facebook_operations, facebook, event_description, details))
        executors.append(executor.submit(
            google_operations, google, event_description, details))
        executors.append(executor.submit(
            email_operations, google, event_description, details))
    for exec in executors:
        print(exec.result())
