from datetime import datetime
import codecs

def getIndex(symbol):
    return ord(symbol)

def getLetter(index):
    return chr(index)

def updateRow(row):
    end = row[:1]
    front = row[1:]
    return (front + end)

def KSA(key):
    Seq = list(range(256))
    j = 0
    for i in range(256):
        j = (j+Seq[i]+key[i%len(key)])%256
        Seq[i], Seq[j] = Seq[j], Seq[i] 
    return Seq

def PRGA(Seq):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + Seq[i]) % 256
        Seq[i], Seq[j] = Seq[j], Seq[i] 
        Key = Seq[(Seq[i] + Seq[j]) % 256]
        yield Key

def RC4(key, text,filetype):
    key = [ord(c) for c in key]
    keystream = PRGA(KSA(key))
    res = []
    if(filetype == ".txt"):
        for c in text:
            val = ("%02X" % (c ^ next(keystream))) 
            res.append(val)
        return ''.join(res)
    val = text ^ next(keystream)
    return val

def encrypt(plaintext, key, filetype):
    if filetype == ".txt":
        plaintext = str(plaintext)
        plaintext = [ord(c) for c in plaintext]
        return RC4(key, plaintext,filetype)
    for i in range(len(plaintext)):
        plaintext[i] = RC4(key,plaintext[i],filetype)
    return plaintext

def decrypt(ciphertext, key, filetype):
    if filetype == ".txt":
        ciphertext = codecs.decode(ciphertext, 'hex_codec')
        res = RC4(key, ciphertext,filetype)
        return codecs.decode(res, 'hex_codec').decode('utf-8')
    for i in range(len(ciphertext)):
        ciphertext[i] = RC4(key,ciphertext[i],filetype)
    return ciphertext

def run(encipher, text, key, filetype):
    if (encipher):
        result = encrypt(text, key, filetype)
        return (result)
    result = decrypt(text, key, filetype)
    return (result)

if __name__ == '__main__':
    text = ""
    ext = ""
    filename = input()
    filetype = "." + (filename.split(".")[1])
    if(ext == ".txt"):
        with open(filename, "r", encoding='utf-8') as current_file:
            text = current_file.read()
            current_file.close()
    else:
        current_file = open(filename, "rb")
        text = [x for x in current_file.read()]
        current_file.close()

    result = run(False,text, key, filetype)
    print(result)
    result = bytes(result)
    filename = "4"
    path = filename + filetype
    if (filetype == ".txt"):
        file = open("../hasil/"+path, 'w')
    else:
        file = open("../hasil/"+path, 'wb')
    file.write(result)
    file.close()
