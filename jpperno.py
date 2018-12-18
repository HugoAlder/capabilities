import os, pwd, grp, time

from http.server import BaseHTTPRequestHandler, HTTPServer
from cgroups import Cgroup

HOST_NAME = 'localhost'
PORT_NUMBER = 80

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/foo': {'status': 200},
            '/bar': {'status': 302},
            '/baz': {'status': 404},
            '/qux': {'status': 500}
        }

        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond({'status': 500})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
        <html><head><title>Title goes here.</title></head>
        <body><p>This is a test.</p>
        <p>You accessed path: {}</p>
        </body></html>
        '''.format(path)
        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)


def drop_privileges(uid_name='nobody', gid_name='nobody'):

    if os.getuid() != 0:
        # We're not root so, like, whatever dude
        return

    # Get the uid/gid from the name
    running_uid = pwd.getpwnam(uid_name).pw_uid
    running_gid = grp.getgrnam(gid_name).gr_gid

    # Remove group privileges
    os.setgroups([])

    # Try setting the new uid/gid
    os.setgid(running_gid)
    os.setuid(running_uid)

    # Ensure a very conservative umask
    old_umask = os.umask(0o77)


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    # Creating cgroup with wanted limitations
    cg = Cgroup('jppapin')
    cg.set_cpu_limit(1)
    cg.set_memory_limit(700, unit="kilobytes")

    # Adding this process in the cgroup
    pid = os.getpid();
    cg.add(pid);

    print("Before dropping privileges")
    drop_privileges()
    print("After dropping privileges")

    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
