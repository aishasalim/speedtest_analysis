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

# # 2.1 the data needs to be gathered every 4 hours
    # Sleep for 6 hours
    # 6 hrs * 4 iteration = 24 hrs / 1 day
    # 16 iterations = 4 days
# # 2.2 this data needs to be into the dictionary format
    # data = {
    #   0: {
    #       "date": YYY-MM-DD,
    #       "time": HH:MM:SS,
    #       "download_speed": SSS,
    #       "upload_speed": SSS
    #   }
    # }
# # 2.3 the data also converts the dictionary to the csv file

while is_enough:
    driver = webdriver.Safari()
    url = 'https://www.speedtest.net/'
    driver.get(url)

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

    upload_speed_list.append(float(upload_speed))
    download_speed_list.append(float(download_speed))

    print(download_speed)
    print(upload_speed)

    current_time = datetime.datetime.now()
    data[counter] = {
        "date": current_time.strftime('%Y-%m-%d'),
        "time": current_time.strftime('%H:%M:%S'),
        "download_speed": float(download_speed),
        "upload_speed": float(upload_speed)
    }

    driver.quit()
    # time.sleep(6 * 60 * 60)

    # Sleep for 6 hours
    # 6 hrs * 4 iteration = 24 hrs
    # 16 iterations = 4 days

    if counter >= 5:
        # break the loop after 3 days of gathering data
        is_enough = False

    counter += 1
    time.sleep(20)

print(data)

# {
# 0: {'date': '2023-08-05', 'time': '16:11:42', 'download_speed': 112.42, 'upload_speed': 23.17},
# 1: {'date': '2023-08-05', 'time': '16:12:54', 'download_speed': 97.48, 'upload_speed': 23.25},
# 2: {'date': '2023-08-05', 'time': '16:14:12', 'download_speed': 102.99, 'upload_speed': 23.3},
# 3: {'date': '2023-08-05', 'time': '16:15:25', 'download_speed': 104.61, 'upload_speed': 23.36},
# 4: {'date': '2023-08-05', 'time': '16:16:38', 'download_speed': 100.85, 'upload_speed': 23.25},
# 5: {'date': '2023-08-05', 'time': '16:17:52', 'download_speed': 111.44, 'upload_speed': 23.09}
# }


# making the CSV file
with open('data.csv', 'w', newline='') as csvfile:
    fieldnames = ['date', 'time', 'download_speed', 'upload_speed']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for key, value in data.items():
        writer.writerow(value)

# NUMBER 3 make a graph out of the data
