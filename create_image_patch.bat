@echo off
python generate_image_data_r.py ^
	-d "data\images" ^
	-o "data\build-images" ^
	-i "lib\ImageMagick-7.0.7-38-portable-Q16-x86\convert.exe" ^
	-n "lib\Narchive-1.0.1\Narchive.exe" ^
	-t "lib\TppkTool-1.0.1\TppkTool.exe" ^
	> logs\cip_generate_image_data_r.txt