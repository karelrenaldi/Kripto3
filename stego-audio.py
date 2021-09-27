import os
import random

def get_payload_size(audio_bytes):
	# mengembalikan ukuran pesan maksimum yang dapat di-embed file audio
	# ukuran file dalam bit
	return max(0, (len(audio_bytes) - 44 - 6) // 8) # 1 byte untuk seed, 5 byte untuk eof

def lsb_embed(audio_bytes, message, seed = 0):
	# mengembalikan audio (array of int) hasil penyisipan pesan
	# KAMUS
	# audio_bytes: array of int [0..256]
	# message: array of int [0..256]

	if get_payload_size(audio_bytes) < len(message)*8:
		raise ValueError("File is not big enough.")

	message = [seed] + message + [35, 35, 35, 35, 35] # concat seed & eof
	print(message)
	# embed
	if seed == 0:
		# sekuensial
		for i in range(0, len(message)):
			for j in range(0, 8):
				if (message[i]&(1<<j)) == 0:
					audio_bytes[44 + 8*i + j] &= (~1 & 0xFF) # turn off bit
				else:
					audio_bytes[44 + 8*i + j] |= 1 # turn on bit
	else:
		# acak
		# taruh seed di depan
		for j in range(0, 8):
			if (message[0]&(1<<j)) == 0:
				audio_bytes[44 + j] &= (~1 & 0xFF) # turn off bit
			else:
				audio_bytes[44 + j] |= 1 # turn on bit
		# shuffle index
		indices = [x for x in range(52, len(audio_bytes))]
		random.Random(seed).shuffle(indices)
		# taruh message
		for i in range(1, len(message)):
			for j in range(0, 8):
				if (message[i]&(1<<j)) == 0:
					audio_bytes[indices[8*(i-1)+j]] &= (~1 & 0xFF) # turn off bit
				else:
					audio_bytes[indices[8*(i-1)+j]] |= 1 # turn on bit

	return audio_bytes

def lsb_extract(audio_bytes):
	# mengembalikan pesan (array of int) yang disisipkan dalam audio
	seed = 0
	for i in range(44, 44+8):
		seed |= (audio_bytes[i]&1)<<(i-44)
	ret = []
	if seed == 0:
		# sekuensial
		i = 0
		while (len(ret) < 5) or (ret[-5:] != [35, 35, 35, 35, 35]):
			add = 0
			for j in range(0, 8):
				if (audio_bytes[52 + 8*i + j]&1) == 1:
					add |= (1<<j)
			ret.append(add)
			i += 1
	else:
		print(seed)
		# acak
		# shuffle index
		indices = [x for x in range(52, len(audio_bytes))]
		random.Random(seed).shuffle(indices)
		i = 0
		while (len(ret) < 5) or (ret[-5:] != [35, 35, 35, 35, 35]):
			add = 0
			for j in range(0, 8):
				if (audio_bytes[indices[8*i+j]]&1) == 1:
					add |= (1<<j)
			ret.append(add)
			i += 1
	return ret[:-5]

# tes = []
# with open("./audio.wav", "rb") as file:
# 	tes = [x for x in file.read()]
# result = lsb_embed(tes, [10, 20, 30], 69)

# with open("./result.wav", "wb") as file:
# 	file.write(bytes(result))

# tes = []
# with open("./result.wav", "rb") as file:
# 	tes = [x for x in file.read()]
# result = lsb_extract(tes)

# print(result)