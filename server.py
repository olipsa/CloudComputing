import configparser
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, urlencode
import cgi

import requests


class handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        query = urlparse(self.path).query
        try:
            query_components = dict(qc.split("=") for qc in query.split("&"))
            print(query_components)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            city = query_components['departure']
            min = int(query_components['min'])
            max = int(query_components['max'])
            try:
                departure, destination = get_result(city, min, max)
                self.wfile.write(bytes(
                    f"<div>Get to <b>{departure['name']}</b>({departure['iata_code']}). Distance: {departure['distance']}</div>"
                    f"<div>Arrive at <b>{destination['name']}</b>({destination['iata_code']}). Distance: {destination['distance']}"
                    f"</div>", 'utf-8'))
            except WebServiceException as e:
                self.wfile.write(bytes(f"<div>{e}</div", 'utf-8'))

        except ValueError:
            print("No query parameters.")
            if self.path == '/':
                self.path = 'index.html'
            if self.path.endswith('/metrics'):
                self.path = 'webservices_logs.txt'
            try:
                file = open(self.path).read()
                self.send_response(200)
            except:
                file = "File not found"
                self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        content_len = int(self.headers.get('Content-length'))
        pdict['Content-length'] = content_len
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            departure = fields.get('departure')[0]
            minimum_distance = fields.get('min')[0]
            maximum_distance = fields.get('max')[0]
            print(departure, minimum_distance, maximum_distance)
            dict = {'departure': str(departure), 'min': minimum_distance, 'max': maximum_distance}
            qstr = urlencode(dict)

        self.send_response(301)
        self.send_header("Content-type", "text/html")
        self.send_header('Location', '/?' + qstr)
        self.end_headers()


class WebServiceException(Exception):
    pass


def get_result(city, min, max):
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get latitude and longitude of provided city
    c = time.time()
    response = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={config['OpenWeatherAPI']['key']}")
    delay = time.time() - c
    logging("OpenWeather API response time: " + str(delay))
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("api.openweathermap")
        raise WebServiceException(err)
    latitude = response.json()[0]['lat']
    longitude = response.json()[0]['lon']

    # Get a random distance in a provided interval
    min_distance = min
    max_distance = max
    c = time.time()
    response = requests.get(f"https://www.random.org/integers/?num=1&min={min_distance}&max={max_distance}"
                            f"&col=1&base=10&format=plain&rnd=new")
    delay = time.time() - c
    logging("Random.org API response time: " + str(delay))
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("random.org")
        raise WebServiceException(err)
    random_distance = response.text

    # Find the nearest airport from current location and airport to a random destination
    c = time.time()
    response = requests.get(
        f"https://airlabs.co/api/v9/nearby?lat={latitude}&lng={longitude}&distance={random_distance}&"
        f"api_key={config['AirLabsAPI']['key']}")
    delay = time.time() - c
    logging("AirLabs API response time: " + str(delay))
    if "error" in json.loads(response.text):
        print("AirLabs")
        raise WebServiceException("AirLabs error: "+response.json()["error"]["message"])
    print(116)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise WebServiceException(err)
    print(121)
    airports = response.json()["response"]['airports']
    print(123)
    destination = None
    departure = None
    for airport in airports:
        if 'iata_code' in airport.keys():
            if departure is None:
                departure = airport
                continue
            destination = airport
    print(132)
    print(departure, destination)
    return departure, destination


def logging(text):
    file = open("webservices_logs.txt", 'a')
    file.write(time.asctime())
    file.write(" " + text + '<br>\n')
    file.close()


def main():
    PORT = 8088
    server = HTTPServer(("", PORT), handler)
    print("Server started at port 8088.")
    server.serve_forever()
    server.server_close()
    print("Server stopped.")


if __name__ == '__main__':
    main()
