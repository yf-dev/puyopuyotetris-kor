@echo off
rem If you change this file, you should change same file on dist directory.
python extract_narc_r.py ^
	-d "data\steam_data" ^
	-n "lib\Narchive-1.0.1\Narchive.exe" ^
	> logs\esta_log_extract_narc_r.txt
python extract_tppk_r.py ^
	-d "data\steam_data" ^
	-t "lib/TppkTool-1.0.1/TppkTool.exe" ^
	> logs\esta_log_extract_narc_r.txt
python convert_dds_to_png_r.py ^
	-d "data\steam_data" ^
	-i "lib/ImageMagick-7.0.7-38-portable-Q16-x86/convert.exe" ^
	> logs\esta_log_convert_dds_to_png_r.txt
python convert_mtx_to_json_r.py ^
	-d "data\steam_data" ^
	-m "lib/PuyoTextEditor-1.0.1/MtxToJson.exe" ^
	> logs\esta_log_convert_mtx_to_json_r.txt
python convert_fif_to_json_r.py ^
	-d "data\steam_data" ^
	> logs\esta_log_convert_fif_to_json_r.txt