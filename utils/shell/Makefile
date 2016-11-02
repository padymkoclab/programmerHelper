#!/bin/bash

COUNT_OBJECTS=`ls -l | egrep -c '^-'`

AUTHOR='Seti Volkylany'
YEAR=$(shell date +'%Y')
MONTH_NUM=$(shell date +'%-m')
DAY_NUM=$(shell date +'%-d')
COPYRIGHT_FORMAT:='%s %d или %d от СМЗХ\n'

COUNT_PATHS = `echo $PATH | sed 's/\:/\n/g' | wc -l`
ONLINE_DISPLAY_PATHS = `$PATH | sed 's/\:/\n/g' | cat -n`
ONLINE_DISPLAY_PATHS = `ls | nl`


all: paths

compile: temp.cpp
	@ g++ -o temp temp.cpp
	@ ./temp

.PHONY: temp
clean: temp
	@ rm temp

paths:
	@ echo '---------PATH--------';
	@ echo $(shell echo $(PATH)) | sed 's/:/\n/g' | nl;
	@ # printf "%s" `$PATH | sed 's/:/\n/g' | nl`

listdir:
	@ printf 'Curent folder "%s" contains %s objects:\n' $(PWD) $(COUNT_OBJECTS);
	@ for obj in $(shell ls); do printf '\t%s\n' $$obj; done

copyright:

	@ \
	if [ $(MONTH_NUM) -gt 9 ]; then \
		printf $(COPYRIGHT_FORMAT) $(AUTHOR) $(YEAR) $(shell expr $(YEAR) + 5509 ); \
	elif [ $(MONTH_NUM) -lt 9 ]; then \
		printf $(COPYRIGHT_FORMAT) $(AUTHOR) $(YEAR) $(shell expr $(YEAR) + 5508 );\
	else \
		if [ $(DAY_NUM) -gt 20 ]; then \
			printf $(COPYRIGHT_FORMAT) $(AUTHOR) $(YEAR) $(shell expr $(YEAR) + 5509 ); \
		else \
			printf $(COPYRIGHT_FORMAT) $(AUTHOR) $(YEAR) $(shell expr $(YEAR) + 5508 ); \
		fi;\
	fi;

sysinfo:
	@ echo 'OS:' `uname --operating-system`;
	@ echo 'Language:' $(LANG);
	@ echo 'Datetime:' `date`;
	@ echo 'User:' $(USER);
