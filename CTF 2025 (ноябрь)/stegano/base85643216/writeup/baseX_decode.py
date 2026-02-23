import base64

def decode_from_baseX(filepath):

    encode_str = open(filepath).read()

    while encode_str.find('FECTF') == -1:
        try:
            encode_str = base64.b16decode(encode_str).decode()
        except: 
            try:
                encode_str = base64.b32decode(encode_str).decode()
            except:
                try:
                    encode_str = base64.b64decode(encode_str).decode()
                except:
                    try:
                        encode_str = base64.b85decode(encode_str).decode()
                    except: break

    return encode_str

filepath = input("\nEnter the path to the file: ")
print("Decoded string:", decode_from_baseX(filepath))
