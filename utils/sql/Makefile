#!/bin/bash

TESTS = $(wildcard *.sql)
REGRESS = $(patsubst %.sql,%,$(TESTS))
REGRESS_OPTS = --load-language plpgsql

all: try_connect show_data

try_connect:
	@ python -m script --try_connect

show_results: script.py
	@ python -m script --show_results

run_tests: script.py
	@ pg_prove --pset tuples_only=1 $(TESTS)

copyright:
	@ echo "Me"
