@echo off
python generate_font_data_r.py ^
	-d "data\generated" ^
	-o "data\build" ^
	-i "lib\ImageMagick-7.0.7-38-portable-Q16-x86\convert.exe" ^
	-n "lib\Narchive-1.0.1\Narchive.exe" ^
	-t "lib\TppkTool-1.0.1\TppkTool.exe" ^
	-f "data\fonts\Binggrae-Bold.otf" ^
	| lib\wtee.exe logs\rcfp_generate_font_data_r.txt

python copy_mtx_r.py ^
	-s "data\generated" ^
	-d "data\build" ^
	| lib\wtee.exe logs\rcfp_copy_mtx_r.txt