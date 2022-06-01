# Server.py
import Pyro4


@Pyro4.expose
class Math(object):
    def Avg(self, x, y, z):
        return (x + y + z) / 3

    def Max(self, x, y, z):
        return max(x, y, z)


daemon = Pyro4.Daemon()        # make a Pyro daemon
uri = daemon.register(Math)   # register the Hello as a Pyro object

print("Server Ready: Object uri =", uri)      # print the uri so we can use it in the client later
daemon.requestLoop()                   # start the event loop of the server to wait for calls
