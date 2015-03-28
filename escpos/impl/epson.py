# -*- coding: utf-8 -*-
#
# escpos/impl/epson.py
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

import time

from ..barcode import BarcodeEAN13
from ..barcode import BarcodeEAN8
from ..barcode import BarcodeCode128


class GenericESCPOS(object):

    device = None
    """
    The device where ESCPOS commands will be written.

    Indeed, it is an instance of a connection that represents a real device on
    the other end. It may be a serial RS232 connection, a bluetooth connection,
    a USB connection, a network connection, or whatever any other way we can
    ``catch`` it, ``write`` to and ``read`` from.
    """


    def __init__(self, device):
        super(GenericESCPOS, self).__init__()
        self.device = device
        self.device.catch()


    def init(self):
        self.device.write('\x1B\x40')


    def lf(self, lines=1):
        """
        Line feed. Issues a line feed to printer *n*-times.
        """
        for i in xrange(lines):
            self.device.write('\x0A')


    def textout(self, text):
        """
        Write text "as-is".
        """
        self.device.write(text)


    def text(self, text):
        """
        Write text followed by a line feed.
        """
        self.textout(text)
        self.lf()


    def text_center(self, text):
        """
        Shortcut method for print centered text.
        """
        self.justify_center()
        self.text(text)


    def justify_center(self):
        self.device.write('\x1B\x61\x01')


    def justify_left(self):
        self.device.write('\x1B\x61\x00')


    def justify_right(self):
        self.device.write('\x1B\x61\x02')


    def set_expanded(self, flag):
        raise NotImplementedError()


    def set_condensed(self, flag):
        raise NotImplementedError()


    def set_emphasized(self, flag):
        raise NotImplementedError()



    def barcode(self, instance):
        """
        Print the given barcode instance, or any other object capable of
        render itself.
        """
        self.device.write(instance.render())
        time.sleep(0.25) # sleeps quarter-second for barcode to be printed
        response = self.device.read()
        return response


    def ean13(self, data, **kwargs):
        """
        Shortcut method for print barcode EAN-13 symbol for the given data.
        """
        code = BarcodeEAN13(data, **kwargs)
        return self.barcode(code)


    def ean8(self, data, **kwargs):
        """
        Shortcut method for print barcode EAN-8 symbol for the given data.
        """
        code = BarcodeEAN8(data, **kwargs)
        return self.barcode(code)


    def code128(self, data, **kwargs):
        """
        Shortcut method for print barcode Code128 symbol for the given data.
        """
        code = BarcodeCode128(data, **kwargs)
        return self.barcode(code)


    def qrcode(self, data, **kwargs):
        """
        Print QRCode symbol for the given data.
        """
        raise NotImplementedError()