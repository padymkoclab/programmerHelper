#!/bin/bash
#
# Usage:
# ./script.sh "mylabour.fields_db" "mylabour.models_fields"

if [ -z "$1" ]; then
    echo "First argument is not passed"
    exit 1
fi

if [ -z "$2" ]; then
    echo "Second argument is not passed"
    exit 1
fi

if [ "$1" == "$2" ]; then
    echo "First and second arguments is equal."
    exit 1
fi

# Displaying a promt to a user
printf """
Your input is next:
    Original text = $1
    Replacable text = $2
Is all right (yes/no): """

# Promt confirmation from the user
read confirm

# if the user agrees
if [ "$confirm" != 'yes' ]; then
    exit 1
fi

# save variables in a environment
export original_text=$1
export text_for_replace=$2

# find only in files with extension *.py in the folder ./apps/.
# The search making by the passed text, recursively
# and return only path to found files.
# Keep the result in a Bash array, the array - in a variable
found_files=($(grep --include=*.py -rl apps/ -e "$original_text"))

# a length the array
count_found_files=${#found_files[@]}

# if the array is not empty
if [ $count_found_files -gt 0 ]; then

    printf "Found $count_found_files files\n"

    # make for loop in the array
    # and replace an all needed fragments of the original text
    # as well display path to a found file
    for (( i = 0; i < $count_found_files; i++ )); do
        sed -i "s/$original_text/$text_for_replace/g" ${found_files[$i]}
        printf "${found_files[$i]}\n"
    done

else
    printf "Nothing found\n"

    # Display files and found fragments of the needed text with numbers of lines
    # Now is not used.
    # grep --include=*.py -rn apps/ -e "$original_text"
fi

# Combination grep and sed. Now is not used.
# grep -nl $tempfile -e "$original_text" | xargs sed -i "s/$original_text/$text_for_replace/g"

# remove the variables from the environment
unset original_text
unset text_for_replace
