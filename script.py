import random
import threading
import time

import requests
status200 = 0
status400 = 0
status404 = 0
status500 = 0
total_time = 0


def get_requests(number):
    global status200, status400, status404, status500, total_time
    locations = ['Iasi', 'London', 'Non-existing-location', 'Madrid']
    routes = ['/', '/metrics', '/non-existing-page']
    departure = random.randrange(0, 4)
    route = random.randrange(0, 3)
    min_km = random.randrange(10, 1000)
    max_km = random.randrange(500, 5000)
    start = time.time()
    url = f"http://localhost:8088{routes[route]}?departure={locations[departure]}&min={min_km}&max={max_km}"
    response = requests.get(url)
    response_time = time.time()-start
    total_time += response_time
    print("Request url:", url)
    print("Status code:", response.status_code, end=" ")
    print("; response time:", response_time, "s ", end=" ")
    print("; text:", response.text,"\n")
    if response.status_code == 200:
        status200 += 1
    elif response.status_code == 400:
        status400 += 1
    elif response.status_code == 404:
        status404 += 1
    elif response.status_code == 500:
        status500 += 1


def main():
    requests_no = input("Number of requests: ")
    batches_no = input("Number of batches: ")
    for i in range(0, int(requests_no), int(batches_no)):
        for j in range(int(batches_no)):
            threading.Thread(target=get_requests, args=(i,)).start()
            time.sleep(1)
    time.sleep(10)
    print(f"\nstatus code 200: {status200} requests, status code 400: {status400} requests,"
          f" status code 404: {status404} requests, status code 500: {status500} requests)")
    print("Average response time: ", total_time/int(requests_no), "s")



if __name__ == '__main__':
    main()
