
TEMP_NAME=`date | md5sum`
TEMP_NAME='_temp_file'

run_c: utils.c
	@ gcc utils.c -o $(TEMP_NAME)
	@ ./$(TEMP_NAME)
	@ rm $(TEMP_NAME)
