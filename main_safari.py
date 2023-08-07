from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import csv
import os
from graph_drawer import GraphDrawer

# ============================= NUMBER 1 set data variables for the code =============================

promised_download = 400
promised_upload = 35

data = []  # Initialized as a list
is_enough = True
counter = 0

# ============================= NUMBER 2 gather that data for 7 days =============================

file_exists = os.path.isfile('data.csv')

while is_enough:
    counter += 1

    driver = webdriver.Safari()
    URL = 'https://www.speedtest.net/'
    driver.get(URL)
    # Navigate to the button "Go!" in Speedtest
    button_div = driver.find_element(By.CLASS_NAME, "start-button")
    button = button_div.find_element(By.TAG_NAME, "a")
    button.click()
    time.sleep(50)

    download_speed = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
    upload_speed = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text

    # Append a new dictionary to the list
    current_time = datetime.datetime.now()
    data_point = {
        "date": current_time.strftime('%Y-%m-%d'),
        "time": current_time.strftime('%H:%M:%S'),
        "download_speed": float(download_speed),
        "upload_speed": float(upload_speed)
    }
    data.append(data_point)  # Add data point to the list

    # Close the window
    driver.quit()

    # create CSV file that will update with dictionary
    with open('data.csv', 'a', newline='') as csvfile:
        fieldnames = ['date', 'time', 'download_speed', 'upload_speed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If the file did not exist previously, write the header
        if not file_exists:
            writer.writeheader()

        writer.writerow(data_point)
    if counter >= 4:  # 28 iterations = 7 days
        # Initialize GraphDrawer here after you've collected some data
        graph_drawer = GraphDrawer(data, promised_download, promised_upload)
        graph_drawer.check_data_and_plot()

    time.sleep(10)
    # 6 hrs break
    # time.sleep(6 * 60 * 60)

    print(data)
