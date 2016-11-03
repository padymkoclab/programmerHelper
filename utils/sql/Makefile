#!/bin/bash

TESTS = $(wildcard tests/*.sql)
REGRESS = $(patsubst tests/%.sql,%,$(TESTS))
REGRESS_OPTS = --load-language plpgsql

all: show_data

connect:
	@ psql -d temp_db -U temp_user -h localhost

try_connect:
	@ python -m script --try_connect

update_db:
	@ python -m script --update_db

show_results: script.py
	@ python -m script --show_results

test: script.py tests/*.sql
	@ bash update_test_plan.sh
	@ pg_prove --dbname temp_db --pset tuples_only=1 $(TESTS) -U postgres --verbose

copyright:
	@ printf " © Seti Volkylany (setivolkylany@gmail.com) from 7525 от СМЗХ.\nMade from soul and with love.\n"
