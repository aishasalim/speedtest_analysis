from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import csv

# ============================= NUMBER 1 get the data from speedtest =============================

# variables from my promised Xfinity plan
promised_download = 600
promised_upload = 35

download_speed_list = []
upload_speed_list = []
data = {}
is_enough = True

counter = 0

# ============================= NUMBER 2 gather that data for 4 days =============================

# # 2.1 The data needs to be gathered every 4 hours
    # Sleep for 6 hours
    # 6 hrs * 4 iteration = 24 hrs / 1 day
    # 16 iterations = 4 days
# # 2.2 This data needs to be into the dictionary format
    # data = {
    #   0: {
    #       "date": YYYY-MM-DD,
    #       "time": HH:MM:SS,
    #       "download_speed": SSS,
    #       "upload_speed": SSS
    #   }
    # }
# # 2.3 The data also converts the dictionary to the CSV file

# Condition for the loop since for now the project is not constantly-updating
while is_enough:
    driver = webdriver.Safari()
    URL = 'https://www.speedtest.net/'
    driver.get(URL)
    # Navigate to the button "Go!" in Speedtest
    button_div = driver.find_element(By.CLASS_NAME, "start-button")
    button = button_div.find_element(By.TAG_NAME, "a")
    button.click()
    time.sleep(50)
    
    download_speed = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div'
                                                   '/div/div[2]/div[3]/div[3]/div/div[3]/div/'
                                                   'div/div[2]/div[1]/div[1]/div/div[2]/span').text
    upload_speed = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3'
                                                 ']/div[3]/div/div[3]/div/div/div[2]/div'
                                                 '[1]/div[2]/div/div[2]/span').text
    
    # Create a dictionary for the data
    current_time = datetime.datetime.now()
    data[counter] = {
        "date": current_time.strftime('%Y-%m-%d'),
        "time": current_time.strftime('%H:%M:%S'),
        "download_speed": float(download_speed),
        "upload_speed": float(upload_speed)
    }
    # Close the window 
    driver.quit()

    if counter >= 16: # 16 iterations = 4 days
        # break the loop after 3 days of gathering data
        is_enough = False

    counter += 1
    # time.sleep(20)
    time.sleep(6 * 60 * 60)

print(data)

# ============================= NUMBER 3 make the CSV file =============================

with open('data.csv', 'w', newline='') as csvfile:
    fieldnames = ['date', 'time', 'download_speed', 'upload_speed']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for key, value in data.items():
        writer.writerow(value)

# ============================= NUMBER 4 make a graph out of the CSV data =============================
