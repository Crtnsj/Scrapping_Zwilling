from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import polars as pl
import time
import re

driver = webdriver.Chrome()


def check_cookies():
    shadow_host = driver.find_element(By.ID, "usercentrics-root")
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)
    WebDriverWait(shadow_root, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[data-testid="uc-accept-all-button"]')
        )
    ).click()


def save_page_source(file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(driver.page_source)


def get_description():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[aria-controls="product-description-panel"]')
            )
        ).click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "product-description-panel"))
        )
        return driver.find_element(By.ID, "product-description-panel").text
    except:
        return ""


def get_teaser():
    try:
        return (
            WebDriverWait(driver, 2)
            .until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".teaser-section__content")
                )
            )
            .text
        )
    except:
        return ""


def get_pics():
    try:
        pics_gallery = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gallery__thumbnails"))
        )
        pics = pics_gallery.find_elements(By.TAG_NAME, "img")

        urls = [
            re.sub(r"(sw=|sh=)\d+", r"\g<1>800", pic.get_attribute("src"))
            for pic in pics
        ]

        return ",".join(urls)
    except:
        pic = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".gallery__main-image"))
        )
        return [re.sub(r"(sw=|sh=)\d+", r"\g<1>800", pic.get_attribute("srcset"))]


def get_chars():
    try:

        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-controls="product-specifications-panel"]'))
            ).click()
            chars_div = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.ID, "product-specifications-panel")
                )
            )
            WebDriverWait(chars_div, 5).until(
            EC.presence_of_element_located((By.XPATH, "(//li)[last()]"))
            )   
            chars = chars_div.find_elements(By.TAG_NAME, "li")
            full_chars = ""
            time.sleep(1)
            for char in chars:
                try:
                    spans = char.find_elements(By.TAG_NAME, "span")
                    char_name = spans[0].text
                    char_value = spans[1].text
                    if char_name != "NO d’article":
                        full_chars += (
                            str.replace(char_name, ":", "")
                            + ": "
                            + str.replace(char_value, ",", ".")
                            + ": 0:1,"
                        )
                except:
                    pass
            time.sleep(1)
        except:
            print("je n'ai pas ouvert du premier coup")
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[aria-controls="product-specifications-panel"]')
                )
            ).click()
            print("j'ai ouvert au deuxième coup")
            chars_div = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.ID, "product-specifications-panel")
                )
            )
            WebDriverWait(chars_div, 5).until(
                EC.presence_of_element_located((By.XPATH, "(//li)[last()]"))
            )
            chars = chars_div.find_elements(By.TAG_NAME, "li")
            full_chars = ""
            time.sleep(1)
            for char in chars:
                try:
                    spans = char.find_elements(By.TAG_NAME, "span")
                    char_name = spans[0].text
                    char_value = spans[1].text
                    if char_name != "NO d’article":
                        full_chars += (
                            str.replace(char_name, ":", "")
                            + ": "
                            + str.replace(char_value, ",", ".")
                            + ": 0:1,"
                        )
                except:
                    pass
            time.sleep(1)
       
        return full_chars
    except Exception as e:
        print(e)
        return ""


def get_data_from_product(url, cookie, ref):
    try:
        article_infos = {}
        driver.get(url)
        if cookie:
            check_cookies()

        article_infos["url"] = url
        article_infos["ref"] = ref
        article_infos["description"] = get_description()
        article_infos["teaser"] = get_teaser()
        article_infos["chars"] = get_chars()
        article_infos["pics"] = get_pics()
        df = pl.DataFrame(article_infos)
        return df
    except:
        pass


def get_data(urls, priceList):
    df = pl.DataFrame(get_data_from_product(urls["url"][0], True, urls["ref"][0]))

    ref_list = set(priceList["REF"].to_list())
    old_ref_list = set(priceList["OLD_REF"].to_list())

    for ref, url in zip(urls["ref"][1:], urls["url"][1:]):
        if ref in ref_list or ref in old_ref_list:
            print(url)
            try:
                df = pl.concat([df, get_data_from_product(url, False, ref)])
            except:
                pass

    return df
