import cv2
import PySimpleGUI as sg
from stego_audio import *
from stego_image import *
import rc4

'''
Theme
'''
sg.theme("DarkTeal12")

'''
Constants
'''
WIN_SIZE = (800, 600)
BTN_SIZE_1 = (40, 2)
BTN_SIZE_2 = (20, 1)
TEXTBOX_SIZE = (40, 2)
MULTILINE_SIZE = (40, 8)
INPUTTEXT_SIZE = (40, 1)
TITLE_SIZE = "28px"

'''
Windows
'''
window_main_menu = [
	[sg.Text("Modified RC4 & Steganography with LSB", size=TEXTBOX_SIZE, justification="center")],
	[sg.Button("Modified RC4", size=BTN_SIZE_1)],
    [sg.Button("Steganography (Embed)", size=BTN_SIZE_1)],
    [sg.Button("Steganography (Extract)", size=BTN_SIZE_1)],
    [sg.Button("Quit", size=BTN_SIZE_1)]
]

window_image_steganography = [
	[sg.Text("Dummy", size=TEXTBOX_SIZE, justification="center")],
	[sg.Button("Back to Main Menu", size=BTN_SIZE_1)]
]

window_steganography_embed = [
	[sg.Text("Embed Message", size=TEXTBOX_SIZE, justification="center")],
	[
		sg.Text("Message:"),
		sg.Radio("Read from textbox", "embed_message_option", key="embed_message_option_1", default=True),
		sg.Radio("Open file as text", "embed_message_option", key="embed_message_option_2"),
		sg.Radio("Open file as binary", "embed_message_option", key="embed_message_option_3")
	],
	[
		sg.Multiline(key="embed_message", size=MULTILINE_SIZE),
		sg.Column([
			[sg.FileBrowse(target="embed_message_filename", button_text="Open message file")],
			[sg.InputText(key="embed_message_filename", size=INPUTTEXT_SIZE)]
		])
	],
	[
		sg.Column([
			[sg.Text("Cover file:"), sg.FileBrowse(target="embed_cover_filename", button_text="Open")],
			[sg.Text("Stego key (positive integer):")],
			[sg.Text("RC4 key :")],
			[sg.Text("Save file as:"), sg.FileSaveAs(target="embed_result_filename", button_text="Save As")]
		]),
		sg.Column([
			[sg.InputText(key="embed_cover_filename", size=INPUTTEXT_SIZE)],
			[sg.InputText(key="embed_stego_key", size=INPUTTEXT_SIZE)],
			[sg.InputText(key="embed_rc4_key", size=INPUTTEXT_SIZE)],
			[sg.InputText(key="embed_result_filename", size=INPUTTEXT_SIZE)]
		])
	],
	[sg.Button("Embed Message in Cover File", size=BTN_SIZE_1)],
	[sg.Button("Back to Main Menu", size=BTN_SIZE_1)]
]

window_steganography_extract = [
	[sg.Text("Extract Message", size=TEXTBOX_SIZE, justification="center")],
	[
		sg.Column([
			[sg.Text("Cover file:"), sg.FileBrowse(target="extract_cover_filename", button_text="Open")],
			[sg.Text("RC4 key :")],
		]),
		sg.Column([
			[sg.InputText(key="extract_cover_filename", size=INPUTTEXT_SIZE)],
			[sg.InputText(key="extract_rc4_key", size=INPUTTEXT_SIZE)]
		])
	],
	[
		sg.Text("Message option:"),
		sg.Radio("Write to textbox", "extract_message_option", key="extract_message_option_1", default=True),
		sg.Radio("Save message as text", "extract_message_option", key="extract_message_option_2"),
		sg.Radio("Save message as binary", "extract_message_option", key="extract_message_option_3")
	],
	[
		sg.Multiline(key="extract_message", size=MULTILINE_SIZE),
		sg.Column([
			[sg.FileSaveAs(target="extract_message_filename", button_text="Save As")],
			[sg.InputText(key="extract_message_filename", size=INPUTTEXT_SIZE)]
		])
	],
	[sg.Button("Extract Message from Cover File", size=BTN_SIZE_1)],
	[sg.Button("Back to Main Menu", size=BTN_SIZE_1)]
]

window_RC4 = [
	[sg.Text("RC4", size=TEXTBOX_SIZE, justification="center")],
	[
		sg.Text("Encrypt / Decrypt"),
		sg.Radio("Encrypt", "RC4_option", key="RC4_option_1", default=True),
		sg.Radio("Decrypt","RC4_option", key="RC4_option_2")
	],
	[
		sg.Text("Message:"),
		sg.Radio("Read from textbox","RC4_message_option", key="RC4_message_option_1", default=True),
		sg.Radio("Open file as text","RC4_message_option", key="RC4_message_option_2"),
		sg.Radio("Open file as binary","RC4_message_option", key="RC4_message_option_3")
	],
	[
		sg.Multiline(key="RC4_File_message", size=MULTILINE_SIZE),
		sg.Column([
			[sg.FileBrowse(target="RC4_message_filename", button_text="Open File")],
			[sg.InputText(key="RC4_message_filename", size=INPUTTEXT_SIZE)]
		])
	],
	[		
		sg.Column([
			[sg.Text("RC4 key :")]
		]),
		sg.Column([
			[sg.InputText(key="RC4_result_message", size=INPUTTEXT_SIZE)]
		])
	],
	[sg.Multiline(key="RC4_Result_message", size=MULTILINE_SIZE)],
	[
		sg.Column([
			[sg.Text("Save file as:"), sg.FileSaveAs(target="RC4_result_filename", button_text="Save As")]
		]),
		sg.Column([
			[sg.InputText(key="RC4_result_filename", size=INPUTTEXT_SIZE)]
		])
	],
	[sg.Button("Run", size=BTN_SIZE_1)],
	[sg.Button("Back to Main Menu", size=BTN_SIZE_1)]
]

all_windows = [
	[
		sg.Column(window_main_menu, key="window_main_menu"),
		sg.Column(window_image_steganography, key="window_image_steganography", visible=False),
		sg.Column(window_steganography_embed, key="window_steganography_embed", visible=False),
		sg.Column(window_RC4, key="window_RC4", visible=False),
		sg.Column(window_steganography_extract, key="window_steganography_extract", visible=False),
	]
]

'''
Event Handlers
'''
def handle_embed_event(values):
	try:
		# get keys
		stego_key = 0
		rc4_key = values["embed_rc4_key"]
		if len(values["embed_stego_key"]) != 0:
			stego_key = int(values["embed_stego_key"])

		# get message
		message = ""
		if values["embed_message_option_1"]:
			# kalo baca dari textbox
			message = values["embed_message"]
		elif values["embed_message_option_2"]:
			# kalo baca file as text
			with open(values["embed_message_filename"], "r") as file:
				message = file.read()
			if message == None:
				raise ValueError("File not found")
		else:
			# kalo baca file as binary
			with open(values["embed_message_filename"], "rb") as file:
				message = file.read()
			if message == None:
				raise ValueError("File not found")

		# encrypt message if needed
		if rc4_key != '':
			if type(message) == str:
				message = rc4.run(True, message, rc4_key, '.txt')
			elif type(message) == bytes:
				message = rc4.run(True, [x for x in message], rc4_key, '.bin')
				message = ''.join([chr(x) for x in message])

		# get cover & embed
		embed_cover_filename = values["embed_cover_filename"]
		psnr = 0
		if embed_cover_filename.endswith(".wav"):
			cover = []
			# kalo cover file audio
			# buka file cover
			with open(values["embed_cover_filename"], "rb") as file:
				cover = [x for x in file.read()]

			# convert message ke array of int
			if type(message) == str:
				message = [ord(x) for x in message]
			elif type(message) == bytes:
				message = [x for x in message]

			# embed
			result = audio_embed(cover, message, stego_key)
			result = bytes(result)

			# save result
			with open(values["embed_result_filename"], "wb") as file:
				file.write(result)

			audio1 = [x for x in open(values["embed_cover_filename"], 'rb').read()]
			audio2 = [x for x in open(values["embed_result_filename"], 'rb').read()]

			psnr = get_audio_psnr(audio1, audio2)
		elif embed_cover_filename.endswith(".png") or embed_cover_filename.endswith(".bmp"):
			image = cv2.imread(values["embed_cover_filename"])

			secret_message = message
			if type(message) == bytes:
				secret_message = ''.join([chr(x) for x in message])

			new_image = lsb_embed(image, secret_message, stego_key)
			cv2.imwrite(values["embed_result_filename"], new_image)

			image1 = cv2.imread(values["embed_cover_filename"])
			image2 = cv2.imread(values["embed_result_filename"])
			psnr = get_image_psnr(image1, image2)
		else:
			raise ValueError('Invalid file extension')

		sg.popup("Embed succesful with psnr : {} dB".format(psnr))

	except ValueError as a:
		sg.popup(a)

def RC4_Func(window,values):
	message = ""
	_, extension = os.path.splitext(values["RC4_message_filename"])

	key =  values["RC4_result_message"]
	if(values["RC4_message_option_1"]):
		message = values["RC4_File_message"]
		extension = ".txt"
	elif(values["RC4_message_option_2"]):
		with open(values["RC4_message_filename"],"r") as file:
			message = file.read()
		if(message == None):
			raise ValueError("File not found")
	else:
		with open(values["RC4_message_filename"],"rb") as file:
			message = [x for x in file.read()]
	if(values["RC4_option_1"]):
		if(extension == ".txt"):
			window["RC4_Result_message"].update(rc4.run(True,message,key,extension))
		else:
			with open(values["RC4_result_filename"], "wb") as file:
				file.write(bytes(rc4.run(True,message,key,extension)))
			sg.popup("File saved succesfully")
	elif(values["RC4_option_2"]):
		if(extension == ".txt"):
			window["RC4_Result_message"].update(rc4.run(False,message,key,extension))
		else:
			with open(values["RC4_result_filename"], "wb") as file:
				file.write(bytes(rc4.run(True,message,key,extension)))
			sg.popup("File saved succesfully")

def handle_extract_event(window, values):
	try:
		# get cover
		cover = []
		extract_cover_filename = values["extract_cover_filename"]
		if extract_cover_filename.endswith(".wav"):
			with open(values["extract_cover_filename"], "rb") as file:
				cover = file.read()
		elif extract_cover_filename.endswith(".png") or extract_cover_filename.endswith(".bmp"):
			cover = cv2.imread(values["extract_cover_filename"])
		else:
			raise ValueError('Invalid file extension')

		# get keys
		rc4_key = values["extract_rc4_key"]

		# extract message
		message = []
		if extract_cover_filename.endswith(".wav"):
			# kalo cover audio
			# convert cover jadi array of int
			cover = [x for x in cover]
			# extract message
			message = audio_extract(cover)
		else:
			message = lsb_extract(cover)
			message = [ord(x) for x in message]

		if values["extract_message_option_1"]:
			# tulis message ke textbox
			message = ''.join([chr(x) for x in message])

			# Decrypt message.
			if rc4_key != '':
				message = rc4.run(False, message, rc4_key, '.txt')

			window["extract_message"].update(message)

		elif values["extract_message_option_2"]:
			# save message as text
			message = ''.join([chr(x) for x in message])

			# Decrypt message.
			if rc4_key != '':
				message = rc4.run(False, message, rc4_key, '.txt')

			with open(values["extract_message_filename"], "w") as file:
				file.write(message)

			sg.popup("File saved succesfully")

		else:
			# Decrypt message.
			if rc4_key != '':
				message = rc4.run(False, message, rc4_key, '.bin')
				
			message = bytes(message)
			with open(values["extract_message_filename"], "wb") as file:
				file.write(message)

			sg.popup("File saved succesfully")

	except ValueError as a:
		sg.popup(a)

'''
Runner
'''
def run_gui():
	window = sg.Window("Modified RC4 & Steganography with LSB", all_windows, size=WIN_SIZE, element_justification="c")

	while True:
		cur_events, cur_values = window.read()

		if "Modified RC4" in cur_events: # kalo tombol "Image Steganography" diteken
			window["window_main_menu"].update(visible=False)
			window["window_RC4"].update(visible=True)

		if "Steganography (Embed)" in cur_events: # kalo tombol "Audio Steganography (Embed)" diteken
			window["window_main_menu"].update(visible=False)
			window["window_steganography_embed"].update(visible=True)

		if "Steganography (Extract)" in cur_events: # kalo tombol "Audio Steganography (Extract)" diteken
			window["window_main_menu"].update(visible=False)
			window["window_steganography_extract"].update(visible=True)

		if "Back to Main Menu" in cur_events: # kalo tombol "Back to Main Menu" diteken
			window["window_image_steganography"].update(visible=False)
			window["window_steganography_embed"].update(visible=False)
			window["window_steganography_extract"].update(visible=False)
			window["window_RC4"].update(visible=False)
			window["window_main_menu"].update(visible=True)

		if "Run" in cur_events:
			RC4_Func(window,cur_values)

		if "Embed Message in Cover File" in cur_events:
			handle_embed_event(cur_values)

		if "Extract Message from Cover File" in cur_events:
			# print(cur_values)
			handle_extract_event(window, cur_values)

		if cur_events == sg.WIN_CLOSED or 'Quit' in cur_events:
			break

	window.close()

run_gui()