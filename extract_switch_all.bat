@echo off
python extract_tzip_r.py ^
	-d "data\switch_romfs" ^
	-q "lib\quickbms\quickbms.exe" ^
	-s "extract_tzip.bms" ^
	> logs\eswa_log_extract_tzip_r.txt
python extract_narc_r.py ^
	-d "data\switch_romfs" ^
	-n "lib\Narchive-1.0.1\Narchive.exe" ^
	> logs\eswa_log_extract_narc_r.txt
python convert_bntx_to_dds_r.py ^
	-d "data\switch_romfs" ^
	-b "lib\BNTX-Extractor-master\bntx_extract.py" ^
	> logs\eswa_log_convert_bntx_to_dds_r.txt
python convert_mtx_to_json_r.py ^
	-d "data\switch_romfs" ^
	-m "lib/PuyoTextEditor-1.0.1/MtxToJson.exe" ^
	> logs\eswa_log_convert_mtx_to_json_r.txt
python convert_fif_to_json_r.py ^
	-d "data\switch_romfs" ^
	> logs\eswa_log_convert_fif_to_json_r.txt