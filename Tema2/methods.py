import json
import cgi
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
            # List all items available
            data = database.select(collection)
        elif len(path_list) == 2:
            # List info about specific item -> with id = path_list[1]
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
    type, pdict = cgi.parse_header(server.headers['content-type'])
    body = server.rfile.read(int(server.headers['content-length']))
    if type == 'application/json' and len(body) != 0:
        data = json.loads(body.decode())
        path_list = path.split('/')
        path_list = list(filter(lambda a: a != '', path_list))
        if len(path_list) == 0:  # homepage request
            server.send_response(405)
            server.send_header("Content-type", "text/html")
            server.end_headers()
        elif len(path_list) == 1:  # create new item on the provided collection
            collection = path_list[0]
            response = database.insert(collection, data)
            if response == 0:  # collection not found
                server.send_response(404)
                server.send_header("Content-type", "text/html")
                server.end_headers()
            elif response == -1:  # item already exists
                server.send_response(409)
                server.send_header("Content-type", "text/html")
                server.end_headers()
            elif response == -2:  # invalid item
                server.send_response(400)
                server.send_header("Content-type", "text/html")
                server.end_headers()
            else:
                server.send_response(200)
                server.send_header("Content-type", "text/html")
                server.end_headers()
                server.wfile.write(bytes(server.path+"/"+str(response), 'utf-8'))
        else:  # collection not found
            server.send_response(404)
            server.send_header("Content-type", "text/html")
            server.end_headers()

    elif type != 'application/json':  # type not implemented
        server.send_response(501)
        server.send_header("Content-type", "text/html")
        server.end_headers()
    else:  # no data to post
        server.send_response(404)
        server.send_header("Content-type", "text/html")
        server.end_headers()


def PUT(server, path, parameters):
    path_list = path.split('/')
    path_list = list(filter(lambda a: a != '', path_list))
    if len(path_list) == 0 or len(path_list) == 1:  # homepage or entire collection
        server.send_response(405)
        server.send_header("Content-type", "text/html")
        server.end_headers()
    else:
        collection = path_list[0]
        type, pdict = cgi.parse_header(server.headers['content-type'])
        body = server.rfile.read(int(server.headers['content-length']))
        data = json.loads(body.decode())
        if type == 'application/json' and len(body) != 0:
            response = database.update(collection, path_list[1], data)
            if response == 0:  # collection not found
                server.send_response(404)
                server.send_header("Content-type", "text/html")
                server.end_headers()
            elif response == -1:  # invalid item
                server.send_response(400)
                server.send_header("Content-type", "text/html")
                server.end_headers()
            elif response == 1:
                server.send_response(200)
                server.send_header("Content-type", "text/html")
                server.end_headers()
        elif type != 'application/json':  # type not implemented
            server.send_response(501)
            server.send_header("Content-type", "text/html")
            server.end_headers()
        else:  # no data to post
            server.send_response(404)
            server.send_header("Content-type", "text/html")
            server.end_headers()


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


