@echo off
rem If you change this file, you should change same file on dist directory.
python convert_text_to_csv.py ^
	--use_suggestion ^
	json ^
	"data\font_data" ^
	"data\font_data\data_steam" ^
	"data\pptko-translation - data.csv"
python generate_data.py ^
	-a "data\font_data" ^
	-b "data\image_data" ^
	-o "data\generated" ^
	-i "lib\ImageMagick-7.0.7-38-portable-Q16-x86\convert.exe" ^
	-m "lib\PuyoTextEditor-1.0.1\MtxToJson.exe" ^
	-n "lib\Narchive-1.0.1\Narchive.exe" ^
	-t "lib\TppkTool-1.0.1\TppkTool.exe" ^
	-f "data\fonts\NotoSansKR-Bold.otf"