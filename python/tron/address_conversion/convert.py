'''
Example code to convert between standard Tron and ETH encodings.
A single test, for the null address, is provided too.
'''

import base58

def tron_address_string_to_hex_string(t_s):
    assert t_s[0] == 'T'
    b = base58.b58decode(t_s)
    s = b[1:-4].hex()
    assert(len(s) == 40)
    return '0x' + s

def hex_string_to_tron_address(s):
    assert(s[0:2].lower() == '0x')
    to_conv = '41' + s[2:]
    return base58.b58encode_check(bytes.fromhex(to_conv)).decode('ascii')

# example
def tron_hex_convert_test():
    eth_null = '0x0000000000000000000000000000000000000000'
    tron_null = 'T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb'
    assert(tron_null == hex_string_to_tron_address(eth_null))
    assert(eth_null == tron_address_string_to_hex_string(tron_null))
