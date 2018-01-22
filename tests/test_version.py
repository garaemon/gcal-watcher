#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of gcal-watcher.
# http://github.com/garaemon/gcal-watcher

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2018, garaemon <garaemon@gmail.com>

from preggy import expect

from gcal_watcher import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        expect(__version__).to_equal('0.1.0')
