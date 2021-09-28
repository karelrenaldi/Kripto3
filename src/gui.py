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
TITLE_SIZE = "28px"

'''
Windows
'''
window_main_menu = [
	[sg.Text("Modified RC4 & Steganography with LSB", size=TEXTBOX_SIZE, justification="center")],
	[sg.Button("Modified RC4", size=BTN_SIZE_1)],
    [sg.Button("Image Steganography", size=BTN_SIZE_1)],
    [sg.Button("Audio Steganography", size=BTN_SIZE_1)],
    [sg.Button("Quit", size=BTN_SIZE_1)]
]

window_image_steganography = [
	[sg.Text("Dummy", size=TEXTBOX_SIZE, justification="center")],
	[sg.Button("Back to Main Menu", size=BTN_SIZE_1)]
]

window_audio_steganography = [
	[sg.Text("Dummy", size=TEXTBOX_SIZE, justification="center")],
	[sg.Button("Back to Main Menu", size=BTN_SIZE_1)]
]

all_windows = [
	[
		sg.Column(window_main_menu, key="window_main_menu"),
		sg.Column(window_image_steganography, key="window_image_steganography", visible=False),
		sg.Column(window_audio_steganography, key="window_audio_steganography", visible=False)
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

		if "Audio Steganography" in cur_events: # kalo tombol "Audio Steganography" diteken
			window["window_main_menu"].update(visible=False)
			window["window_image_steganography"].update(visible=True)

		if "Back to Main Menu" in cur_events: # kalo tombol "Back to Main Menu" diteken
			window["window_image_steganography"].update(visible=False)
			window["window_audio_steganography"].update(visible=False)
			window["window_main_menu"].update(visible=True)

		if cur_events == sg.WIN_CLOSED or 'Quit' in cur_events:
			break

	window.close()

run_gui()