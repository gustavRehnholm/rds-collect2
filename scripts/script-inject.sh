#!/bin/bash

# files with the stdout, 
# mostly used for troubleshooting and getting meta information (How many files used for what)

# make files that shows what the stdout was 
#rm -f -r rds-collect2/parser/stdout-dir/inject

touch rds-collect2/parser/stdout-dir/inject/output-inject-itr-1355.txt
touch rds-collect2/parser/stdout-dir/inject/output-inject-itr-685.txt
touch rds-collect2/parser/stdout-dir/inject/output-inject-itr-342.txt
touch rds-collect2/parser/stdout-dir/inject/output-inject-itr-230.txt

touch rds-collect2/parser/stdout-dir/inject/output-inject-rnd-1355.txt
touch rds-collect2/parser/stdout-dir/inject/output-inject-rnd-685.txt
touch rds-collect2/parser/stdout-dir/inject/output-inject-rnd-342.txt
touch rds-collect2/parser/stdout-dir/inject/output-inject-rnd-230.txt

touch rds-collect2/parser/stdout-dir/inject/output-inject-none-1355.txt
touch rds-collect2/parser/stdout-dir/inject/output-inject-none-685.txt
touch rds-collect2/parser/stdout-dir/inject/output-inject-none-342.txt
touch rds-collect2/parser/stdout-dir/inject/output-inject-none-230.txt


# test injection with different captures sizes
script -q -c "python3 rds-collect2/parser/inject.py 1355 itr" /dev/null | tee rds-collect2/parser/stdout-dir/inject/output-inject-itr-1355.txt &
script -q -c "python3 rds-collect2/parser/inject.py 685 itr" /dev/null | tee rds-collect2/parser/stdout-dir/inject/output-inject-itr-685.txt &
script -q -c "python3 rds-collect2/parser/inject.py 342 itr" /dev/null | tee rds-collect2/parser/stdout-dir/inject/output-inject-itr-342.txt &
script -q -c "python3 rds-collect2/parser/inject.py 230 itr" /dev/null | tee rds-collect2/parser/stdout-dir/inject/output-inject-itr-230.txt &

#script -q -c "python3 rds-collect2/parser/inject.py 1355 rnd" /dev/null | tee rds-collect2/parser/stdout-dir/inject/output-inject-rnd-1355.txt &
#script -q -c "python3 rds-collect2/parser/inject.py 685 rnd"  /dev/null | tee rds-collect2/parser/stdout-dir/inject/output-inject-rnd-685.txt &
#script -q -c "python3 rds-collect2/parser/inject.py 342 rnd"  /dev/null | tee rds-collect2/parser/stdout-dir/inject/output-inject-rnd-342.txt &
#script -q -c "python3 rds-collect2/parser/inject.py 230 rnd"  /dev/null | tee rds-collect2/parser/stdout-dir/inject/output-inject-rnd-230.txt &

script -q -c "python3 rds-collect2/parser/inject.py 1355 none" /dev/null | tee rds-collect2/parser/stdout-dir/inject/output-inject-none-1355.txt &
script -q -c "python3 rds-collect2/parser/inject.py 685 none" /dev/null | tee rds-collect2/parser/stdout-dir/inject/output-inject-none-685.txt &
script -q -c "python3 rds-collect2/parser/inject.py 342 none" /dev/null | tee rds-collect2/parser/stdout-dir/inject/output-inject-none-342.txt &
script -q -c "python3 rds-collect2/parser/inject.py 230 none" /dev/null | tee rds-collect2/parser/stdout-dir/inject/output-inject-none-230.txt &
wait