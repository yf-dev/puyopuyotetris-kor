@echo off
pyinstaller --onefile convert_fif_json.py
pyinstaller --onefile convert_original_data.py
pyinstaller --onefile convert_text_to_csv.py
pyinstaller --onefile generate_data.py
pyinstaller --onefile generate_font_data.py