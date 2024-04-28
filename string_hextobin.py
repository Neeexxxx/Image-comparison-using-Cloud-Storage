def hexStr_to_binStr(str_hex):
    my_hexdata = str_hex
    scale = 16 ## equals to hexadecimal
    num_of_bits = 8
    return bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)
