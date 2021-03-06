# -*- coding: utf8 -*-

# CRC16Kermit (CRC-CCITT (Kermit)) MODULE
#
# Autor: Cristian NAVALICI cristian.navalici at gmail dot com
#        Modificado por Matias Novoa
# Año: 2014
# Licencia: GNU/GPL V3 http://www.gnu.org/copyleft/gpl.html

from ctypes import c_ushort


class CRC16Kermit(object):
    crc16kermit_tab = []

    # The CRC's are computed using polynomials.
    # Here is the most used coefficient for CRC16 SICK
    crc16Kermit_constant = 0x8408

    def __init__(self):
        if not(self.crc16kermit_tab):
            self.init_crc16kermit()  # initialize the precalculated tables

    def calculate(self, string=''):
        '''Calculate a CRC-CCITT(Kermit) for hexadecimal string and returns a
        decimal value'''
        try:
            if not isinstance(string, str):
                raise Exception(
                    "Please provide a string as argument for calculation.")
            if not string:
                return 0

            crcValue = 0x0000
            c = ''
            for d in string:
                c += d
                if len(c) == 2:
                    short_c = 0x00ff & c_ushort(int(c, 16)).value
                    tmp = crcValue ^ short_c
                    crcValue = c_ushort(
                        crcValue >> 8).value ^ int(
                        self.crc16kermit_tab[(tmp & 0xff)], 0)
                    c = ''

            # After processing, the one's complement of
            # the CRC is calcluated and the two bytes of the CRC are swapped.
            low_byte = (crcValue & 0xff00) >> 8
            high_byte = (crcValue & 0x00ff) << 8
            crcValue = low_byte | high_byte

            return crcValue
        except Exception as e:
            print(("EXCEPTION(calculate): {}".format(e)))

    def get_crc(self, string=''):
        '''return a list of string with de low byte and the high byte of
        crcValue'''
        hexa = hex(self.calculate(string))
        crcl = hexa[:-2]
        crch = hexa[:2] + hexa[-2:]
        return [crcl, crch]

    def init_crc16kermit(self):
        '''The algorithm use tables with precalculated values'''
        for i in range(0, 256):
            crc = c_ushort(i).value
            for j in range(0, 8):
                if (crc & 0x0001):
                    crc = c_ushort(crc >> 1).value ^ self.crc16Kermit_constant
                else:
                    crc = c_ushort(crc >> 1).value
            self.crc16kermit_tab.append(hex(crc))
