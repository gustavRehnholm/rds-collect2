#!/bin/bash

# files with the stdout, 
# mostly used for troubleshooting and getting meta information (How many files used for what)
#touch stdout-dir/output-inject-itr-1370.txt
#touch stdout-dir/output-inject-ittr-685.txt
#touch stdout-dir/output-inject-ittr-342.txt
#touch stdout-dir/output-inject-ittr-171.txt

#touch stdout-dir/output-inject-rnd-1370.txt
#touch stdout-dir/output-inject-rnd-685.txt
#touch stdout-dir/output-inject-rnd-342.txt
#touch stdout-dir/output-inject-rnd-171.txt

#rm stdout-dir/output-inject-none-1370.txt
#rm stdout-dir/output-inject-none-685.txt
rm stdout-dir/output-inject-none-342.txt
rm stdout-dir/output-inject-none-200.txt

#touch stdout-dir/output-inject-none-1370.txt
#touch stdout-dir/output-inject-none-685.txt
touch stdout-dir/output-inject-none-342.txt
touch stdout-dir/output-inject-none-200.txt


# test injection with different captures sizes
#script -q -c "python3 inject.py 1370 itr" /dev/null | tee stdout-dir/output-inject-itr-1370.txt
#script -q -c "python3 inject-ittr.py 685" /dev/null | tee stdout-dir/output-inject-ittr-685.txt
#script -q -c "python3 inject-ittr.py 342" /dev/null | tee stdout-dir/output-inject-ittr-342.txt
#script -q -c "python3 inject-ittr.py 171" /dev/null | tee stdout-dir/output-inject-ittr-171.txt

#script -q -c "python3 inject.py 1370 rnd" /dev/null | tee stdout-dir/output-inject-rnd-1370.txt
#script -q -c "python3 inject-rnd.py 685" /dev/null | tee stdout-dir/output-inject-rnd-685.txt
#script -q -c "python3 inject-rnd.py 342" /dev/null  | tee stdout-dir/output-inject-rnd-342.txt
#script -q -c "python3 inject-rnd.py 171" /dev/null  | tee stdout-dir/output-inject-rnd-171.txt

#script -q -c "python3 inject.py 1370 none" /dev/null | tee stdout-dir/output-inject-none-1370.txt
#script -q -c "python3 inject.py 685 none" /dev/null | tee stdout-dir/output-inject-none-685.txt
script -q -c "python3 inject.py 342 none" /dev/null | tee stdout-dir/output-inject-none-342.txt
script -q -c "python3 inject.py 200 none" /dev/null | tee stdout-dir/output-inject-none-200.txt
