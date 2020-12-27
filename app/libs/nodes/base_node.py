import logging
import os
from abc import abstractmethod

from flask import current_app


class BaseNode:
    allow_input = []

    def __init__(self, id_, node_type, project_id, in_edges, out_edges):
        self.id = id_
        self.node_type = node_type
        self.project_id = project_id
        self.in_edges = in_edges
        self.out_edges = out_edges
        # shape
        self.input_shape = None
        self.output_shape = None
        # logger
        self.logger = logging.getLogger('node-{}'.format(id_))
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(
            logging.FileHandler(self.join_path('log.txt'), mode='w')
        )

    def dictionary_path(self, id_=None):
        return '{}/{}/node/{}'.format(
            current_app.config['FILE_DIRECTORY'], self.project_id,
            self.id if id_ is None else id_
        )

    def join_path(self, filename, id_=None):
        return os.path.join(self.dictionary_path(id_), filename)

    @abstractmethod
    def run(self):
        pass

    def run_train(self):
        return self.run()

    def run_test(self):
        return self.run()

    @staticmethod
    def get_output(input_):
        return input_
