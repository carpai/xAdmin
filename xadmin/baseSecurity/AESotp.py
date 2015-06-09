# -*- encoding:utf-8 -*-
__author__ = 'playpeng'

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

import codecs
import string, random
import os,binascii
import base64

def StrIDGen(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def RandomStr(size=8):
    return binascii.b2a_hex(os.urandom(size))

def GenerateSalt(size=8):
    return codecs.encode(PBKDF2('xAdminPassphase', RandomStr(size)), 'hex')

# AES Cipher
class AESCipher():
    def __init__(self, key):
        # default AES block size
        self.bs = AES.block_size

        # OTP key
        self.key = key

        # mix key
        self.iv = RandomStr(int(self.bs/2))

    def getotpkey(self):
        return self.key

    def getiv(self):
        return self.iv

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * '\x00'

    def _unpad(self, s):
       return s[:-ord(s[len(s)-1:])]

    def expsalt(self):
        exp = self.iv + self.key
        return base64.b64encode(exp)

    """
        AES encryption support Unicode string.
    """
    def encryptUTF8Str(self, msg):
        # NOTE: don't move cipher to __int__, encrypt and decrypt can't share with
        # one cipher
        #  DO NOT CALL encrypt or decrypt more than once!!.
        #  FIXME: Does this will work to replace <base64 encoding unicode string>?
        #     -- rawstr = str(codecs.encode(bytes(msg, encoding="utf8"), 'hex'), encoding='utf8')
        rawstr = base64.b64encode(bytes(msg, encoding="utf8")).decode()
        raw = self._pad(rawstr)
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv, segment_size=128)
        ciphertxt = cipher.encrypt(raw)
        return base64.b64encode(ciphertxt)

    # enc is encrypted base64 bytes of unicode string.
    def decryptUTF8Str(self, enc):
        raw = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv, segment_size=128)
        encstr = cipher.decrypt(raw).decode()
        return base64.b64decode(encstr).decode()

    def encryptAscii(self, msg):
        # NOTE: don't move cipher to __int__, encrypt and decrypt can't share with
        # one cipher.
        raw = self._pad(msg)
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv, segment_size=128)
        print(cipher.encrypt(raw))
        return base64.b64encode(cipher.encrypt(raw))

    # enc is encrypted bytes.
    def decryptAscii(self, enc):
        raw = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv, segment_size=128)
        txt = cipher.decrypt(raw)
        return self._unpad(txt)
