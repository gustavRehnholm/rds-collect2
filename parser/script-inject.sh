#!/bin/bash

# files with the stdout, 
# mostly used for troubleshooting and getting meta information (How many files used for what)
#touch stdout-dir/output-inject-ittr-1370.txt
touch stdout-dir/output-inject-rnd-685.txt
touch stdout-dir/output-inject-rnd-342.txt
touch stdout-dir/output-inject-rnd-171.txt

#touch stdout-dir/output-inject-rnd-1370.txt
#touch stdout-dir/output-inject-rnd-685.txt
#touch stdout-dir/output-inject-rnd-342.txt
#touch stdout-dir/output-inject-rnd-171.txt

# test injection with different captures sizes
#script -q -c "python3 inject-ittr.py 1370" /dev/null | tee stdout-dir/output-inject-ittr-1370.txt
script -q -c "python3 inject-ittr.py 685" /dev/null | tee stdout-dir/output-inject-ittr-685.txt
script -q -c "python3 inject-ittr.py 342" /dev/null | tee stdout-dir/output-inject-ittr-342.txt
script -q -c "python3 inject-ittr.py 171" /dev/null | tee stdout-dir/output-inject-ittr-171.txt

#python3 inject-rnd.py 1370 | tee stdout-dir/output-inject-rnd-1370.txt
#python3 inject-rnd.py 685 | tee stdout-dir/output-inject-rnd-685.txt
#python3 inject-rnd.py 342 | tee stdout-dir/output-inject-rnd-342.txt
#python3 inject-rnd.py 171 | tee stdout-dir/output-inject-rnd-171.txt
