import hashlib, codecs

def sha256HashStr(str):
    return hashlib.sha256(codecs.encode(str)).hexdigest()
