# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Module tests."""

from __future__ import absolute_import, print_function

import pkg_resources
from flask import Flask
from flask_login import current_user
from mock import patch

from invenio_cache import InvenioCache, cached_unless_authenticated, \
    current_cache, current_cache_ext
from invenio_cache.ext import _callback_factory


def test_version():
    """Test version import."""
    from invenio_cache import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    app.config.update(CACHE_TYPE='simple')
    ext = InvenioCache(app)
    assert 'invenio-cache' in app.extensions

    app = Flask('testapp')
    app.config.update(CACHE_TYPE='simple')
    ext = InvenioCache()
    assert 'invenio-cache' not in app.extensions
    ext.init_app(app)
    assert 'invenio-cache' in app.extensions


def test_cache(app):
    """Test current cache proxy."""
    current_cache.set('mykey', 'myvalue')
    assert current_cache.get('mykey') == 'myvalue'


def test_current_cache(app):
    """Test current cache proxy."""
    current_cache.set('mykey', 'myvalue')
    assert current_cache.get('mykey') == 'myvalue'


def test_current_cache_ext(app):
    """Test current cache proxy."""
    assert app.extensions['invenio-cache'] \
        == current_cache_ext._get_current_object()


def test_callback():
    """Test callback factory."""
    # Default (current_user from flask-login)
    assert _callback_factory(None) is not None
    # Custom callable
    assert _callback_factory(lambda: 'custom')() == 'custom'
    # Import string
    assert _callback_factory('invenio_cache.cached_unless_authenticated') == \
        cached_unless_authenticated


@patch('pkg_resources.get_distribution')
def test_callback_no_login(get_distribution):
    """Test callback factory (no flask-login)."""
    get_distribution.side_effect = pkg_resources.DistributionNotFound
    assert _callback_factory(None)() is False
