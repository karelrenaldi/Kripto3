import PySimpleGUI as sg
from stego_audio import *
from rc4 import *

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
			[sg.Text("RC4 key (positive integer):")],
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
			[sg.Text("RC4 key (positive integer):")],
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
			[sg.FileBrowse(target="extract_message_filename", button_text="Open message file")],
			[sg.InputText(key="extract_message_filename", size=INPUTTEXT_SIZE)]
		])
	],
	[sg.Button("Extract Message from Cover File", size=BTN_SIZE_1)],
	[sg.Button("Back to Main Menu", size=BTN_SIZE_1)]
]

all_windows = [
	[
		sg.Column(window_main_menu, key="window_main_menu"),
		sg.Column(window_image_steganography, key="window_image_steganography", visible=False),
		sg.Column(window_steganography_embed, key="window_steganography_embed", visible=False),
		sg.Column(window_steganography_extract, key="window_steganography_extract", visible=False)
	]
]

'''
Event Handlers
'''
def handle_embed_event(values):
	try:
		# get keys
		stego_key = 0
		if len(values["embed_stego_key"]) != 0:
			stego_key = int(values["embed_stego_key"])
		rc4_key = values["embed_rc4_key"]

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


		# get cover & embed
		cover = []
		if values["embed_cover_filename"].endswith(".wav"):
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
			sg.popup("Embed succesful")

	except ValueError as a:
		sg.popup(a)

def handle_extract_event(window, values):
	try:
		# get cover
		cover = []
		with open(values["extract_cover_filename"], "rb") as file:
			cover = file.read()

		# get keys
		rc4_key = values["extract_rc4_key"]

		# extract message
		message = []
		if values["extract_cover_filename"].endswith(".wav"):
			# kalo cover audio
			# convert cover jadi array of int
			cover = [x for x in cover]
			# extract message
			message = audio_extract(cover)

		if values["extract_message_option_1"]:
			# tulis message ke textbox
			message = ''.join([chr(x) for x in message])
			window["extract_message"].update(message)

		elif values["extract_message_option_2"]:
			# save message as text
			message = ''.join([chr(x) for x in message])
			with open(values["extract_message_filename"], "w") as file:
				file.write(message)
			sg.popup("File saved succesfully")

		else:
			# save message as binary
			message = bytes(message)
			with open(values["extract_message_filename"], "rb") as file:
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
			window["window_main_menu"].update(visible=True)

		if "Embed Message in Cover File" in cur_events:
			# print(cur_values)
			handle_embed_event(cur_values)

		if "Extract Message from Cover File" in cur_events:
			# print(cur_values)
			print("yey")
			handle_extract_event(window, cur_values)

		if cur_events == sg.WIN_CLOSED or 'Quit' in cur_events:
			break

	window.close()

run_gui()