# -*- coding: utf-8 -*-
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler, Application, RedirectHandler
from utils import MainHandler
from processing import ImageProcessHandler
from settings import SERVER_CONF, SERVER_DEFAULT_PAGE, DEFAULT_PORT, DEBUG, VERSION, LOCAL_STORAGE_PATH


class ImageProcessingServer():
    """
    REST API image processing server
    """

    def __init__(self, local_storage=True, port=None): 
        """
        Create IPS Object
        """
        self._debug = DEBUG
        self._port = port if port is not None else DEFAULT_PORT
        self._settings = SERVER_CONF
        self._default_page = SERVER_DEFAULT_PAGE
        self._local_storage = local_storage
        self._local_storage_path = LOCAL_STORAGE_PATH

        self._handlers = [
            (r"/", MainHandler, dict(default_page=self._default_page, params={'storage_mode': self._local_storage,
                                                                              'version': VERSION})),
            (r"/process/", ImageProcessHandler, dict(local_path=self._local_storage_path,
                                                     local_storage=self._local_storage,
                                                     render_type='json',
                                                     debug=self._debug)),
            (r"/process", RedirectHandler, dict(url='/process/', permanent=False))]

        if self._local_storage:
            storage_handler = (r"/getimg/(.*)", StaticFileHandler,
                               dict(path=self._settings['static_path']))
            self._handlers.append(storage_handler)

        self._server = Application(self._handlers, **self._settings)

        if self._debug: 
            print 'Tornado IPS instance %s ready[DEBUG MODE]' % VERSION
            print 'Started on port %d' % self._port

    def run(self): 
        """
        Run tornado IOLoop
        """
        self._server.listen(self._port)
        IOLoop.instance().start()

    def get_port(self): 
        return self._port

    def uses_local_storage(self): 
        return self._local_storage

if __name__ == "__main__": 
    i = ImageProcessingServer()
    i.run()