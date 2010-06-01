import xmlrpclib
import httplib

def Server(url, *args, **kwargs):
   t = TimeoutTransport()
   t.timeout = kwargs.get('timeout', 20)
   if 'timeout' in kwargs:
       del kwargs['timeout']
   kwargs['transport'] = t
   server = xmlrpclib.Server(url, *args, **kwargs)
   return server

class TimeoutTransport(xmlrpclib.Transport):

   def make_connection(self, host):
       conn = TimeoutHTTP(host)
       conn.set_timeout(self.timeout)
       return conn

class TimeoutHTTPConnection(httplib.HTTPConnection):

   def connect(self):
       httplib.HTTPConnection.connect(self)
       # check whether socket timeout support is available (Python >= 2.3)
       try:
           self.sock.settimeout(self.timeout)
       except AttributeError:
           pass

class TimeoutHTTP(httplib.HTTP):
   _connection_class = TimeoutHTTPConnection

   def set_timeout(self, timeout):
       self._conn.timeout = timeout
