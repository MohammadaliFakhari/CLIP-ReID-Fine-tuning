# encoding: utf-8
"""
@author:  sherlock
@contact: sherlockliao01@gmail.com
"""

import glob
import re
import pandas as pd
import os.path as osp

from .bases import BaseImageDataset
from collections import defaultdict
import pickle
class DESTRE(BaseImageDataset):
    dataset_dir = ''

    def __init__(self, root='', verbose=True, pid_begin = 0, **kwargs):
        super(DESTRE, self).__init__()
        self.dataset_dir = osp.join(root, self.dataset_dir)
        self.train_dir = osp.join(self.dataset_dir, 'bounding_box_train')
        self.query_dir = osp.join(self.dataset_dir, 'query')
        self.gallery_dir = osp.join(self.dataset_dir, 'bounding_box_test')

        self._check_before_run()
        self.pid_begin = pid_begin
        train = self._process_dir(self.train_dir, relabel=True)
        query = self._process_dir(self.query_dir, relabel=False)
        gallery = self._process_dir(self.gallery_dir, relabel=False)

        if verbose:
            print("=> DESTRE loaded")
            self.print_dataset_statistics(train, query, gallery)

        self.train = train
        self.query = query
        self.gallery = gallery

        self.num_train_pids, self.num_train_imgs, self.num_train_cams, self.num_train_vids = self.get_imagedata_info(self.train)
        self.num_query_pids, self.num_query_imgs, self.num_query_cams, self.num_query_vids = self.get_imagedata_info(self.query)
        self.num_gallery_pids, self.num_gallery_imgs, self.num_gallery_cams, self.num_gallery_vids = self.get_imagedata_info(self.gallery)

    def _check_before_run(self):
        """Check if all files are available before going deeper"""
        if not osp.exists(self.dataset_dir):
            raise RuntimeError("'{}' is not available".format(self.dataset_dir))
        if not osp.exists(self.train_dir):
            raise RuntimeError("'{}' is not available".format(self.train_dir))
        if not osp.exists(self.query_dir):
            raise RuntimeError("'{}' is not available".format(self.query_dir))
        if not osp.exists(self.gallery_dir):
            raise RuntimeError("'{}' is not available".format(self.gallery_dir))

    def _process_dir(self, dir_path, relabel=False):
        img_paths = glob.glob(osp.join(dir_path, '*.jpg'))
        pattern = re.compile(r'([-\d]+)_c([\d]+)')

        if relabel == False:
            pid_container = set()
            for img_path in sorted(img_paths):
                pid, _ = map(int, pattern.search(img_path).groups())
                if pid == -1: continue  # junk images are just ignored
                pid_container.add(pid)
            pid2label = {pid: label for label, pid in enumerate(pid_container)}
            dataset = []
            for img_path in sorted(img_paths):
                pid, camid = map(int, pattern.search(img_path).groups())
                if relabel: pid = pid2label[pid]
                dataset.append((img_path, self.pid_begin + pid, camid, 0))
            return dataset
        else:
            pid_container = set()
            for img_path in sorted(img_paths):
                pid, _ = map(int, pattern.search(img_path).groups())
                if pid == -1: continue  # junk images are just ignored
                pid_container.add(pid)
            pid2label = {pid: label for label, pid in enumerate(pid_container)}
            dataset = []
            for img_path in sorted(img_paths):
                pid, camid = map(int, pattern.search(img_path).groups())
                if relabel: pid = pid2label[pid]
                dataset.append((img_path, self.pid_begin + pid, camid, 0))
            return dataset
