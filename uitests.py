#!/usr/bin/env python3
# Copyright 2024 QuIC
#
# SPDX-License-Identifier: BSD-3-Clause


from argparse import ArgumentParser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, JavascriptException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


def login(driver, username, passphrase, domain):
    # login
    print(f"Logging into: https://app.{domain}/login/")
    driver.get(f"https://app.{domain}/login/")
    email = driver.find_element(by=By.NAME, value="email")
    password = driver.find_element(by=By.NAME, value="password")
    login_button = driver.find_element(by=By.NAME, value="login")

    email.send_keys(username)
    password.send_keys(passphrase)
    driver.save_screenshot('login.png')
    login_button.click()
    driver.implicitly_wait(5)


def close_video_banner(driver):
    # close initial tutorial
    driver.implicitly_wait(1)
    driver.save_screenshot('close.png')
    try:
        close = driver.find_element(by=By.XPATH, value="//button[.='Close']")
        close.click()
    except NoSuchElementException:
        print("Welcome screen not available")
        pass


def create_factory(driver, args):
    factory_name = args.factory_name
    factory_machine = args.factory_machine
    cancel = args.name_check_only
    print(f"Creating factory for {args.factory_machine}")
    print(f"Factory name: {args.factory_name}")
    # create a factory
    create_button = driver.find_element(by=By.XPATH, value="//button[.='New Factory']")
    create_button.click()

    factory_name_input = driver.find_element(by=By.NAME, value="factoryName")
    factory_name_input.send_keys(factory_name)
    platform_select = Select(driver.find_element(by=By.NAME, value="platform"))
    #try:
    platform_select.select_by_visible_text(factory_machine)
    #except:

    try:
        eula_checkbox = driver.find_element(by=By.XPATH, value="//input[@name='eula']")
        eula_checkbox.click()

    except NoSuchElementException:
        pass

    try:
        checkmark_displayed = driver.find_element(by=By.CLASS_NAME, value="has-text-success")
    except NoSuchElementException:
        print("Factory name invalid")
        return

    wait = WebDriverWait(driver, timeout=5)
    wait.until(lambda d : checkmark_displayed.is_displayed())

    if not cancel:
        next_button = driver.find_element(by=By.XPATH, value="//button[.='Create Factory']")
        next_button.click()
    else:
        cancel_button = driver.find_element(by=By.XPATH, value="//button[.='Cancel']")
        cancel_button.click()

    driver.implicitly_wait(5)


def update_token(driver, args):
    token_name = args.token_name
    print(f"Updating token: {token_name}")
    driver.save_screenshot('profile.png')
    profile_picture = driver.find_element(by=By.XPATH, value="//img[@alt='Profile picture']")

    hover = ActionChains(driver).move_to_element(profile_picture)
    hover.perform()

    settings_link = driver.find_element(by=By.XPATH, value="//a[.='Settings']")
    settings_link.click()

    tokens_link = driver.find_element(by=By.XPATH, value="//a[.='Api tokens']")
    tokens_link.click()

    token_table = driver.find_element(by=By.TAG_NAME, value="table")
    rows = token_table.find_elements(by=By.TAG_NAME, value="tr")
    for row in rows:
        try:
            row.find_element(by=By.XPATH, value=f"//td[text()='{token_name}']")

            token_edit = row.find_element(by=By.CLASS_NAME, value="fa-ellipsis-v")
            token_hover = ActionChains(driver).move_to_element(token_edit)
            token_hover.perform()
            break

        except NoSuchElementException:
            continue

    edit_button = driver.find_element(by=By.XPATH, value="//button[.='Edit']")
    edit_button.click()

    driver.implicitly_wait(5)
    # find factory select
    factory_select = driver.find_element(by=By.XPATH, value="//select[@name='factories[]']")
    select_obj = Select(factory_select)
    for option in select_obj.options:
        option_value = option.get_property("value")
        try:
            select_obj.select_by_value(option_value)
        except JavascriptException:
            print("Exception")
            driver.save_screenshot('token_exception.png')

    save_button = driver.find_element(by=By.XPATH, value="//button[.='Save']")
    save_button.click()


def main():
    parser = ArgumentParser()
    parser.add_argument("--username", required=True, help="Username for logging into FoundriesFactory")
    parser.add_argument("--password", required=True)
    parser.add_argument("--enterprise-domain", default="foundries.io", help="Domain name when using on FF Enterprise")
    subparsers = parser.add_subparsers()
    create = subparsers.add_parser("createfactory", help="Create FF")
    create.add_argument("--factory-name", required=True)
    create.add_argument("--factory-machine", required=True)
    create.add_argument("--name-check-only", action="store_true", default=False, help="Presses cancel button after validating factory name")
    create.set_defaults(func=create_factory)

    update = subparsers.add_parser("updatetoken", help="Update token to add all Factories to scope")
    update.add_argument("--token-name", required=True)
    update.set_defaults(func=update_token)

    args = parser.parse_args()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920,1080)
    login(driver, args.username, args.password, args.enterprise_domain)
    close_video_banner(driver)
    args.func(driver, args)
    driver.close()


if __name__ == "__main__":
    main()
