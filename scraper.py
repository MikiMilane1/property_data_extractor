from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException

import logging

from selenium.webdriver.common.by import By
import pandas as pd
import datetime as dt

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)

data = []

driver.get('https://imovina.net/statistika_cena_nekretnina/')

# REJECT COOKIES
cookies_overlay = driver.find_element(By.ID, "kolacici")
reject_button = cookies_overlay.find_element(By.ID, "odbaci")
reject_button.click()

selection_fields = driver.find_element(By.XPATH, "//div[@class='okolo container']")

year_dropdown = Select(driver.find_element(By.ID, "yearId"))
year_options = year_dropdown.options

for year in range(len(year_options)):

    year_dropdown = Select(driver.find_element(By.ID, "yearId"))
    year_dropdown.select_by_index(year)
    logging.warning(f"Now scraping year {year_dropdown.options[year].text}")

    date_dropdown = Select(driver.find_element(By.XPATH, "//select[@name='stats']"))
    date_options = date_dropdown.options

    submit_button = driver.find_element(By.XPATH, "//input[@class='sbmt']")
    submit_button.click()

    for date in range(len(date_options)):

        date_dropdown = Select(driver.find_element(By.XPATH, "//select[@name='stats']"))
        try:
            date_dropdown.select_by_index(date)
            date = date_dropdown.first_selected_option.text
            logging.warning(f"Now scraping date {date}")
            # CONVERT DATE TO DATETIME OBJECT
            date_format = "%d.%m.%Y"
            date = dt.datetime.strptime(date, date_format)

            submit_button = driver.find_element(By.XPATH, "//input[@class='sbmt']")
            submit_button.click()
            test_element = driver.find_element(By.XPATH, "//p[1]")

            table = driver.find_element(By.XPATH, "//table")
            data_rows = table.find_elements(By.XPATH, ".//tbody/tr")
            locations_and_prices = []
            for row in data_rows:
                try:
                    location = row.find_element(By.XPATH, "./td[1]").text.strip().title()
                    if location == 'Reon':
                        pass
                    else:
                        one_bedroom = row.find_element(By.XPATH, "./td[3]").text
                        two_bedroom = row.find_element(By.XPATH, "./td[5]").text
                        three_bedroom = row.find_element(By.XPATH, "./td[7]").text

                        mean_price = row.find_element(By.XPATH, "./td[8]").text
                        if mean_price == '-':
                            mean_price = None
                        else:
                            pass
                        list_entry = {
                            'location': location,
                            'district': district,
                            'one_br_price': one_bedroom,
                            'two_br_price': two_bedroom,
                            'three_br_price': three_bedroom,
                        }
                        locations_and_prices.append(list_entry)
                except:
                    district = row.find_element(By.XPATH, "./td[1]").text
                district = district.replace('OPŠTINA ', '').strip().title()

            for entry in locations_and_prices:
                data.append(({
                    'location': entry['location'],
                    'district': entry['district'],
                    'date': date,
                    'price': entry['mean_price'],
                }))
        except NoSuchElementException:
            pass

df = pd.DataFrame(data)
df.to_csv('scraped_data.csv', index=False)
driver.quit()
