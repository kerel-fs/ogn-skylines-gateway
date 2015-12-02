# SkyLines - the free internet platform for sharing flights
# Copyright (C) 2012-2013  The SkyLines Team (see AUTHORS.md)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Source: https://github.com/skylines-project/skylines/blob/master/skylines/tracking/crc.py

import struct
from crc16 import crc16xmodem


def calc_crc(data):
    assert len(data) >= 16

    crc = crc16xmodem(data[:4])
    crc = crc16xmodem(b'\0\0', crc)
    crc = crc16xmodem(data[6:], crc)
    return crc


def check_crc(data):
    assert len(data) >= 16

    crc1 = calc_crc(data)
    crc2 = struct.unpack_from('!H', data, 4)[0]
    return crc1 == crc2


def set_crc(data):
    assert len(data) >= 16

    crc = calc_crc(data)
    return data[:4] + struct.pack('!H', crc) + data[6:]
