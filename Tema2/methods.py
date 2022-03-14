import json

import database


def GET(server, path, parameters):
    # print("Path:", path)
    # print("Params:", parameters)
    path_list = path.split('/')
    path_list = list(filter(lambda a: a != '', path_list))
    if len(path_list) == 0:   # homepage request
        server.send_response(200)
        server.send_header("Content-type", "text/html")
        server.end_headers()
    else:
        collection = path_list[0]
        data = []
        if len(path_list) == 1:
            # List all books available
            data = database.select(collection)
        elif len(path_list) == 2:
            # List info about specific book -> with id = path_list[1]
            data = database.select(collection, ID=path_list[1])

        if len(path_list) > 2 or len(data) == 0:  # if URL invalid or collection/item not found
            server.send_response(404)
            server.send_header("Content-type", "text/html")
            server.end_headers()
        else:
            server.send_response(200)
            server.send_header("Content-type", "text/html")
            server.end_headers()
            response = json.dumps(data)
            server.wfile.write(response.encode("UTF-8"))


def POST(server, path, parameters):
    pass


def PUT(server, path, parameters):
    pass


def DELETE(server, path, parameters):
    path_list = path.split('/')
    path_list = list(filter(lambda a: a != '', path_list))
    if len(path_list) == 0 or len(path_list) == 1:  # homepage or entire collection
        server.send_response(405)
        server.send_header("Content-type", "text/html")
        server.end_headers()
    else:
        collection = path_list[0]
        if database.delete(collection, path_list[1]) == 0:
            # collection/item not found
            server.send_response(404)
            server.send_header("Content-type", "text/html")
            server.end_headers()
        else:
            server.send_response(200)
            server.send_header("Content-type", "text/html")
            server.end_headers()


