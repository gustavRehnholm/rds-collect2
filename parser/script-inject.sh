#!/bin/bash

# files with the stdout, 
# mostly used for troubleshooting and getting meta information (How many files used for what)
rm stdout-dir/output-inject-itr-1370.txt
rm stdout-dir/output-inject-itr-685.txt
rm stdout-dir/output-inject-itr-342.txt
rm stdout-dir/output-inject-itr-220.txt

touch stdout-dir/output-inject-itr-1370.txt
touch stdout-dir/output-inject-itr-685.txt
touch stdout-dir/output-inject-itr-342.txt
touch stdout-dir/output-inject-itr-220.txt

rm stdout-dir/output-inject-rnd-1370.txt
rm stdout-dir/output-inject-rnd-685.txt
rm stdout-dir/output-inject-rnd-342.txt
rm stdout-dir/output-inject-rnd-220.txt

touch stdout-dir/output-inject-rnd-1370.txt
touch stdout-dir/output-inject-rnd-685.txt
touch stdout-dir/output-inject-rnd-342.txt
touch stdout-dir/output-inject-rnd-220.txt

#rm stdout-dir/output-inject-none-1370.txt
#rm stdout-dir/output-inject-none-685.txt
#rm stdout-dir/output-inject-none-342.txt
#rm stdout-dir/output-inject-none-220.txt

#touch stdout-dir/output-inject-none-1370.txt
#touch stdout-dir/output-inject-none-685.txt
#touch stdout-dir/output-inject-none-342.txt
#touch stdout-dir/output-inject-none-220.txt


# test injection with different captures sizes
script -q -c "python3 inject.py 1370 itr" /dev/null | tee stdout-dir/output-inject-itr-1370.txt
script -q -c "python3 inject.py 685 itr" /dev/null | tee stdout-dir/output-inject-itr-685.txt
script -q -c "python3 inject.py 342 itr" /dev/null | tee stdout-dir/output-inject-itr-342.txt
script -q -c "python3 inject.py 220 itr" /dev/null | tee stdout-dir/output-inject-itr-220.txt

script -q -c "python3 inject.py 1370 rnd" /dev/null | tee stdout-dir/output-inject-rnd-1370.txt
script -q -c "python3 inject.py 685 rnd"  /dev/null | tee stdout-dir/output-inject-rnd-685.txt
script -q -c "python3 inject.py 342 rnd"  /dev/null | tee stdout-dir/output-inject-rnd-342.txt
script -q -c "python3 inject.py 220 rnd"  /dev/null | tee stdout-dir/output-inject-rnd-220.txt

#script -q -c "python3 inject.py 1370 none" /dev/null | tee stdout-dir/output-inject-none-1370.txt
#script -q -c "python3 inject.py 685 none" /dev/null | tee stdout-dir/output-inject-none-685.txt
#script -q -c "python3 inject.py 342 none" /dev/null | tee stdout-dir/output-inject-none-342.txt
#script -q -c "python3 inject.py 220 none" /dev/null | tee stdout-dir/output-inject-none-220.txt
