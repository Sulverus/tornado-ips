# -*- coding: utf-8 -*-
from tornado.web import RequestHandler, asynchronous, HTTPError
from tornado.gen import coroutine, Task, engine
from utils import DEFAULT_RESPONSE
from wrapper import imgProcessingWrapperPIL
from datetime import datetime
import multiprocessing
import json


class ImageProcessHandler(RequestHandler): 
    """
    Main image processing handler
    """
    def initialize(self, local_storage, local_path, render_type='json', debug=False): 
        self._local_storage_mode = local_storage
        self._load_dir = local_path
        self._render = render_type
        self._debug = debug
        self._queue = multiprocessing.Queue()

    @staticmethod
    def create_and_process(queue, path, actions): 
        processor = imgProcessingWrapperPIL(path)
        queue.put(processor.process_actions(actions,
                                            ImageProcessHandler.ips_final_callback,
                                            path))

    @staticmethod
    def ips_final_callback(data):
        print '[%s]:Task %s is done' % (datetime.now().strftime("%d.%m.%Y|%H:%M:%S"), data)

    def get(self): 
        """
        Only post data accept
        """
        self.write(DEFAULT_RESPONSE)

    def post(self): 
        """
        Post request handler
        """
        try:
            post_body = json.loads(self.request.body)
        except:
            raise HTTPError(400)

        request_format = post_body.get('command_type', None)
        actions = post_body.get('actions', None)

        if request_format is None or actions is None:
            raise HTTPError(400)

        if 'filename' not in request_format.keys():
            raise HTTPError(400)

        img_worker = multiprocessing.Process(target=self.create_and_process,
                                             args=(self._queue, request_format['filename'], actions))
        img_worker.start()
        response = {'state': 200, 'data': 'accepted'}
        if self._debug:
            print '[%s]:Queue addition(%d actions) for file: %s from node %s' % (
                datetime.now().strftime("%d.%m.%Y|%H:%M:%S"),
                len(actions),
                request_format['filename'],
                self.request.remote_ip)
        self.write(json.dumps(response))
