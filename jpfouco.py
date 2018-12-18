import os, pwd, grp

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

import SimpleHTTPServer
import SocketServer

PORT = 80

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

m = SimpleHTTPServer.SimpleHTTPRequestHandler.extensions_map
m[''] = 'text/plain'
m.update(dict([(k, v + ';charset=UTF-8') for k, v in m.items()]))

os.system("capsh --print")
print("Before dropping capabilities")

drop_privileges()

os.system("capsh --print")
print("After dropping capabilities")

print("serving at port", PORT)
httpd.serve_forever()
