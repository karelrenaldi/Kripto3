import PySimpleGUI as sg

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
    [sg.Button("Image Steganography", size=BTN_SIZE_1)],
    [sg.Button("Audio Steganography (Embed)", size=BTN_SIZE_1)],
    [sg.Button("Audio Steganography (Extract)", size=BTN_SIZE_1)],
    [sg.Button("Quit", size=BTN_SIZE_1)]
]

window_image_steganography = [
	[sg.Text("Dummy", size=TEXTBOX_SIZE, justification="center")],
	[sg.Button("Back to Main Menu", size=BTN_SIZE_1)]
]

window_audio_steganography_embed = [
	[sg.Text("Embed Message", size=TEXTBOX_SIZE, justification="center")],
	[
		sg.Text("Message:"),
		sg.Radio("Textbox", "message_option", default=True),
		sg.Radio("File as text", "message_option"),
		sg.Radio("File as binary", "message_option")
	],
	[
		sg.Multiline(key="message", size=MULTILINE_SIZE)
	],
	[sg.FileBrowse(target="message_filename", button_text="Open message file")],
	[sg.InputText(key="message_filename", size=INPUTTEXT_SIZE)],
	[
		sg.Column([
			[sg.Text("Cover file:"), sg.FileBrowse(target="embed_cover_audio_filename", button_text="Open")],
			[sg.Text("Stego key (positive integer):")],
			[sg.Text("RC4 key (positive integer):")]
		]),
		sg.Column([
			[sg.InputText(key="embed_cover_audio_filename", size=INPUTTEXT_SIZE)],
			[sg.InputText(key="stego_key", size=INPUTTEXT_SIZE)],
			[sg.InputText(key="embed_rc4_key", size=INPUTTEXT_SIZE)]
		])
	],
	[sg.Button("Embed", size=BTN_SIZE_1)],
	[sg.Button("Back to Main Menu", size=BTN_SIZE_1)]
]

window_audio_steganography_extract = [
	[sg.Text("Extract Message", size=TEXTBOX_SIZE, justification="center")],
	[
		sg.Column([
			[sg.Text("Cover file:"), sg.FileBrowse(target="extract_cover_audio_filename", button_text="Open")],
			[sg.Text("RC4 key (positive integer):")]
		]),
		sg.Column([
			[sg.InputText(key="extract_cover_audio_filename", size=INPUTTEXT_SIZE)],
			[sg.InputText(key="extract_rc4_key", size=INPUTTEXT_SIZE)]
		])
	],
	[sg.Button("Extract", size=BTN_SIZE_1)],
	[sg.Button("Back to Main Menu", size=BTN_SIZE_1)]
]

all_windows = [
	[
		sg.Column(window_main_menu, key="window_main_menu"),
		sg.Column(window_image_steganography, key="window_image_steganography", visible=False),
		sg.Column(window_audio_steganography_embed, key="window_audio_steganography_embed", visible=False),
		sg.Column(window_audio_steganography_extract, key="window_audio_steganography_extract", visible=False)
	]
]

'''
Runner
'''
def run_gui():
	window = sg.Window("Modified RC4 & Steganography with LSB", all_windows, size=WIN_SIZE, element_justification="c")

	while True:
		cur_events, cur_values = window.read()

		if "Image Steganography" in cur_events: # kalo tombol "Image Steganography" diteken
			window["window_main_menu"].update(visible=False)
			window["window_image_steganography"].update(visible=True)

		if "Audio Steganography (Embed)" in cur_events: # kalo tombol "Audio Steganography (Embed)" diteken
			window["window_main_menu"].update(visible=False)
			window["window_audio_steganography_embed"].update(visible=True)

		if "Audio Steganography (Extract)" in cur_events: # kalo tombol "Audio Steganography (Extract)" diteken
			window["window_main_menu"].update(visible=False)
			window["window_audio_steganography_extract"].update(visible=True)

		if "Back to Main Menu" in cur_events: # kalo tombol "Back to Main Menu" diteken
			window["window_image_steganography"].update(visible=False)
			window["window_audio_steganography_embed"].update(visible=False)
			window["window_audio_steganography_extract"].update(visible=False)
			window["window_main_menu"].update(visible=True)

		if cur_events == sg.WIN_CLOSED or 'Quit' in cur_events:
			break

	window.close()

run_gui()