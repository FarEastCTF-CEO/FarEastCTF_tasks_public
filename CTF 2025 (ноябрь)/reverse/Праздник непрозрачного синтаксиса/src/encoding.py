def encode_flag_old_way(flag):
    return ''.join(chr(ord(c) ^ 42 ^ 13) for c in flag)

print(encode_flag_old_way("FECTF{ioccc_enjoyer}"))