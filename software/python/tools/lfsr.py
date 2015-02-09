"""Propeller LFSR Byte Packer

1 = t  | 0111111111
0 = 2t | 0011111111

"""
LFSR_SEED = ord("P")

def lfsr(seed):
    """Generate bits from 8-bit LFSR with taps at 0xB2."""
    while True:
        yield seed & 0x01
        seed = ((seed << 1) & 0xfe) | (((seed >> 7) ^ (seed >> 5) ^ (seed >> 4) ^ (seed >> 1)) & 1)

lfsr_seq = []
for (i, value) in zip(range(500), lfsr(LFSR_SEED)):
    lfsr_seq.append(value)

handshake = [1,0]

handshake += lfsr_seq[:250]

'''
handshake.append('C')

for i in range(258):
    handshake.append(1)
    handshake.append(0)

response = lfsr_seq[249:]
'''


"""Serial has a start bit which is always 0
Serial has a stop bit which is, by necessity, always 1

Between these bits we have 8 bits we can toggle.

0________1

Within this scheme we can pack 5 low pulses of length t like so:

0101010101
_-_-_-_-_-

Or 3 low pulses of length 2t like so:

0010010011
__-__-__--
"""

def pack_bitstream(seq):
	packed = ['']
	bit = None
	while len(seq):
	  byte = packed[len(packed)-1]
	  if bit == None:
	  	bit = seq.pop(0)
	  if bit == 'C':
	  	packed[len(packed)-1] = '1' * 8
	  	packed.append('')
	  	bit = None
	  	continue
	  if bit: # We have a 1, t, or '0'
	    if len(byte) == 0:
	      byte += '1'
	      packed[len(packed)-1] = byte
	      bit = None
	      continue

	    # Pass the bit onto the next byte
	    if len(byte) == 8:
	      packed.append('')
	      continue

	    byte += '0'
	    if len(byte) < 8:
	    	byte += '1'

	    packed[len(packed)-1] = byte
	    bit = None

	    if len(byte) == 8 and len(seq) > 0:
	      packed.append('')

	  else: # We have a 2, 2t, or '00'
	    if len(byte) == 0:
	      byte += '01'
	      packed[len(packed)-1] = byte
	      bit = None
	      continue

	    if len(byte) > 6:
	      packed[len(packed)-1] = byte.ljust(8,'1')
	      packed.append('')
	      continue

	    byte += '00'
	    if len(byte) < 8:
	      byte += '1'

	    packed[len(packed)-1] = byte
	    bit = None

	    if len(byte) == 8 and len(seq) > 0:
	      packed.append('')

	packed[len(packed)-1] = packed[len(packed)-1].ljust(8,'1')

	#print(len(packed))
	print('0' + '1,0'.join(packed) + '1')
	return list(int(i[::-1],2) for i in packed)

print(handshake)
print(','.join(hex(i) for i in pack_bitstream(handshake)))

'''
print(response)
print(','.join(hex(i) for i in pack_bitstream(response)))
'''

exit()

f = open('Analog.binary','rb')
binary = f.read()
f.close()

byte_len = len(binary)


def column(title, text):
	print(title.ljust(30) + ': ' + text)

column('Binary file length', str(byte_len) + ' bytes')

bit_list = []
for byte in binary:
	b = list(bin(ord(byte)).replace('0b','').rjust(8,'0'))
	bit_list += b


bit_list = map(int,bit_list)

bit_len = len(bit_list)

column( 'Length in (above*8)', str(bit_len) + ' bits')

#print(bit_list)

#print(','.join(hex(i) for i in pack_bitstream(bit_list)))

packed_stream = pack_bitstream(bit_list)

packed_len = len(packed_stream)

column( 'Packed lenth', str(packed_len) + ' bytes')

column( 'Compression factor from bits', str( float(bit_len)/float(packed_len) ) )
column( 'Compression factor from bytes', str( float(packed_len)/float(byte_len) ) )


   
