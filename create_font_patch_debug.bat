@echo off
python convert_csv_to_mtx_json_r.py ^
	-d "data\generated" ^
	-c "data\text_edited.csv" ^
	-l "kr" ^
	-p "English" ^
	--offset_64bit ^
	--debug ^
	> logs\cfp_convert_csv_to_mtx_json_r.txt

python convert_json_to_mtx_r.py ^
	-d "data\generated" ^
	-m "lib\PuyoTextEditor-1.0.1\MtxToJson.exe" ^
	> logs\cfp_convert_json_to_mtx_r.txt

python copy_font_data_r.py ^
	-s "data\steam_data" ^
	-d "data\generated" ^
	> logs\cfp_copy_font_data_r.txt

python generate_font_data_r.py ^
	-d "data\generated" ^
	-o "data\build" ^
	-i "lib\ImageMagick-7.0.7-38-portable-Q16-x86\convert.exe" ^
	-n "lib\Narchive-1.0.1\Narchive.exe" ^
	-t "lib\TppkTool-1.0.1\TppkTool.exe" ^
	-f "data\fonts\Binggrae-Bold.otf" ^
	> logs\cfp_generate_font_data_r.txt

python copy_mtx_r.py ^
	-s "data\generated" ^
	-d "data\build" ^
	> logs\cfp_copy_mtx_r.txt