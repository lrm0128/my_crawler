#!/usr/bin/env python
# coding=utf-8

import logging

logs = logging
logs.basicConfig(
    format='%(asctime)s %(filename)s [line: %(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='w',
)
