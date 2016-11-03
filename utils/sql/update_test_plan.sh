#!/bin/bash


FOLDER_WITH_TESTS='tests';

for file_with_tests in "$FOLDER_WITH_TESTS"/*
    do
        TOTAL_COUNT_SELECT=$(grep '^SELECT' $file_with_tests | wc -l);

        # exclude line SET PLAN and SELECT FROM FINISH;
        COUNT_TESTS=$(expr "$TOTAL_COUNT_SELECT" - 2);

        # update a plan of count tests
        $(sed -i -- 's/SELECT plan.*/SELECT plan('"$COUNT_TESTS"');/g' "$file_with_tests");
    done
