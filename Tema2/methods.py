def GET(server, path, parameters):
    print(path)
    print(parameters)

    server.send_response(200)
    server.send_header("Content-type", "text/html")
    server.end_headers()