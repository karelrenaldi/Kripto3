import os
import random
import math

def bytes_to_arrint(_bytes):
	return [x for x in _bytes]

def arrint_to_bytes(arr_int):
	return bytes(arr_int)

def get_audio_payload_size(audio_bytes):
	'''
	Mengembalikan ukuran pesan maksimum yang dapat di-embed file audio.
	Ukuran file dalam bit.
	'''
	return max(0, (len(audio_bytes) - 44 - 6) // 8) # 1 byte untuk seed, 5 byte untuk eof

def get_audio_psnr(audio_bytes_1, audio_bytes_2):
	'''
	Mengembalikan peak-signal-to-noise antara dua file audio (bytes atau array of int).
	Dua file audio harus berukuran sama.
	'''
	if type(audio_bytes_1) == bytes:
		audio_bytes_1 = bytes_to_arrint(audio_bytes_1)
	if type(audio_bytes_2) == bytes:
		audio_bytes_2 = bytes_to_arrint(audio_bytes_2)
	diff_sum = 0
	for i in range(44, len(audio_bytes_1)):
		diff_sum += abs(audio_bytes_1[i] - audio_bytes_2[i])
	rms = (diff_sum / (len(audio_bytes_1) - 44)) ** 0.5
	psnr = 20 * math.log(255/rms)
	return psnr

def audio_embed(audio_bytes, message, seed = 0):
	'''
	mengembalikan audio (bytes) hasil penyisipan pesan
	KAMUS
	audio_bytes: bytes OR array of int [0..256]
	message: bytes OR array of int [0..256]
	'''
	# convert params to array of int
	if type(audio_bytes) == bytes:
		audio_bytes = self.bytes_to_arrint(audio_bytes)
	if type(message) == bytes:
		message = bytes_to_arrint(message)

	if get_audio_payload_size(audio_bytes) < len(message)*8:
		raise ValueError("File is not big enough.")

	# taruh seed di depan
	for j in range(0, 8):
		if (seed&(1<<j)) == 0:
			audio_bytes[44 + j] &= (~1 & 0xFF) # turn off bit
		else:
			audio_bytes[44 + j] |= 1 # turn on bit

	# embed
	message = message + [35, 35, 35, 35, 35] # concat seed & eof
	if seed == 0: # sekuensial
		for i in range(0, len(message)):
			for j in range(0, 8):
				if (message[i]&(1<<j)) == 0:
					audio_bytes[52 + 8*i + j] &= (~1 & 0xFF) # turn off bit
				else:
					audio_bytes[52 + 8*i + j] |= 1 # turn on bit
	else: # acak
		# shuffle index
		indices = [x for x in range(52, len(audio_bytes))]
		random.Random(seed).shuffle(indices)
		# taruh message
		for i in range(0, len(message)):
			for j in range(0, 8):
				if (message[i]&(1<<j)) == 0:
					audio_bytes[indices[8*i + j]] &= (~1 & 0xFF) # turn off bit
				else:
					audio_bytes[indices[8*i + j]] |= 1 # turn on bit

	return arrint_to_bytes(audio_bytes)

def audio_extract(audio_bytes):
	'''
	mengembalikan pesan (bytes) yang disisipkan dalam audio
	'''
	# convert param to array of int
	if type(audio_bytes) == bytes:
		audio_bytes = bytes_to_arrint(audio_bytes)

	# extract message
	seed = 0
	for i in range(44, 44+8):
		seed |= (audio_bytes[i]&1)<<(i-44)
	ret = []
	if seed == 0: # sekuensial
		i = 0
		while (len(ret) < 5) or (ret[-5:] != [35, 35, 35, 35, 35]):
			add = 0
			for j in range(0, 8):
				if (audio_bytes[52 + 8*i + j]&1) == 1:
					add |= (1<<j)
			ret.append(add)
			i += 1
	else: # acak
		# shuffle index
		indices = [x for x in range(52, len(audio_bytes))]
		random.Random(seed).shuffle(indices)
		i = 0
		while (len(ret) < 5) or (ret[-5:] != [35, 35, 35, 35, 35]):
			add = 0
			for j in range(0, 8):
				if (audio_bytes[indices[8*i + j]]&1) == 1:
					add |= (1<<j)
			ret.append(add)
			i += 1
	return ret[:-5]

# tes = []
# with open("./audio.wav", "rb") as file:
# 	tes = [x for x in file.read()]
# result = audio_embed(tes, [10, 20, 69], 69)

# with open("./result.wav", "wb") as file:
# 	file.write(bytes(result))

# tes = []
# with open("./result.wav", "rb") as file:
# 	tes = [x for x in file.read()]
# result = audio_extract(tes)

# a1 = []
# with open("./audio.wav", "rb") as file:
# 	a1 = [x for x in file.read()]
# a2 = []
# with open("./result.wav", "rb") as file:
# 	a2 = [x for x in file.read()]
# print(get_audio_psnr(a1, a2))
# # print(get_audio_psnr(a1, a1))
