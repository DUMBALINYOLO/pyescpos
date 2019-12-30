# -*- coding: utf-8 -*-
#
# escpos/impl/elgin.py
#
# Copyright 2015 Base4 Sistemas Ltda ME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from .. import feature
from ..constants import CASHDRAWER_DEFAULT_DURATION
from ..helpers import as_char
from ..helpers import _Model
from .epson import GenericESCPOS


"""
`Elgin <http://www.elgin.com.br/>`_ ESC/POS printer implementation.
"""


_VENDOR = 'Elgin S/A'


class ElginGeneric(GenericESCPOS):
    """
    Base implementation for Elgin ESC/POS mini-printers.
    """

    model = _Model(name='Generic Elgin', vendor=_VENDOR)

    def __init__(self, device, features={}):
        super(ElginGeneric, self).__init__(device)
        self.hardware_features.update({
                feature.CUTTER: False,
                feature.CASHDRAWER_PORTS: True,
                feature.CASHDRAWER_AVAILABLE_PORTS: 1,
            })
        self.hardware_features.update(features)


class ElginI9(ElginGeneric):
    """Implementation for Elgin i9 thermal mini-printer."""

    model = _Model(name='Elgin I9', vendor=_VENDOR)

    def __init__(self, device, features={}):
        super(ElginI9, self).__init__(device)
        self.hardware_features.update({feature.CUTTER: True})
        self.hardware_features.update(features)

    def set_expanded(self, flag):
        w = 1 if flag else 0  # magnification (Nx)
        self.set_text_size(w, 0)

    def set_condensed(self, flag):
        # 00h = character font A (12x24, normal)
        # 01h = character font B (9x17, condensed)
        param = b'\x01' if flag else b'\x00'
        self.device.write(b'\x1B\x4D' + param)

    def _kick_drawer_impl(self, port=0, **kwargs):
        # param 'm' 0x00 or 0x30 (0, 48) for pin 2
        # param 'm' 0x01 or 0x31 (1, 49) for pin 5
        pin = b'\x00' if port == 0 else b'\x01'

        # pulse duration (0 <= duration <= 255)
        # [1] although the manual says that t1 and t2 should lie in between 0
        # and 255, if t1 is a very low value the drawer may not be kicked!
        duration = kwargs.get('duration', CASHDRAWER_DEFAULT_DURATION)
        t1 = kwargs.get('t1', b'\x20')  # 32ms (t1 should be less than t2) [1]
        t2 = kwargs.get('t2', None) or as_char(ord(t1) + duration)
        self.device.write(b'\x1B\x70' + pin + t1 + t2)


class ElginI7(ElginI9):
    """Implementation for Elgin i7 thermal mini-printer."""

    model = _Model(name='Elgin I7', vendor=_VENDOR)

    def __init__(self, device, features={}):
        super(ElginI7, self).__init__(device)
        self.hardware_features.update({feature.CUTTER: False})
        self.hardware_features.update(features)


class ElginRM22(ElginI9):
    """Implementation for Elgin RM-22 portable thermal printer."""

    model = _Model(name='Elgin RM-22', vendor=_VENDOR)

    def __init__(self, device, features={}):
        super(ElginRM22, self).__init__(device)
        self.hardware_features.update({
                feature.CUTTER: False,
                feature.CASHDRAWER_PORTS: False,
                feature.CASHDRAWER_AVAILABLE_PORTS: 0,
                feature.PORTABLE: True,
                feature.COLUMNS: feature.Columns(
                        normal=32,
                        expanded=16,
                        condensed=42),
            })
        self.hardware_features.update(features)

    def _kick_drawer_impl(self, port=0, **kwargs):
        # honor cash-drawer absence behavior (do nothing)
        pass
