from threadedHTTPServer import ThreadedHTTPServer
from handler import Handler

if __name__ == '__main__':
    port = 1710
    server = ThreadedHTTPServer(('localhost', port), Handler)
    print('Starting server on port ' + str(port))
    server.serve_forever()
