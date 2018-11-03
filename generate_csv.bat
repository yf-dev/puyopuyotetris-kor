@echo off
python convert_text_to_csv_r.py ^
	-d "data\steam_data" ^
	-c "data\text_steam.csv" ^
	| lib\wtee.exe logs\gcst_convert_text_to_csv_r.txt
python convert_text_to_csv_r.py ^
	-d "data\switch_romfs" ^
	-c "data\text_switch.csv" ^
	| lib\wtee.exe logs\gcsw_convert_text_to_csv_r.txt
