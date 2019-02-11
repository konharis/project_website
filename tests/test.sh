#!/bin/bash

echo $1 $2 $3 ' -> echo $1 $2 $3'

# We can also store arguments from bash command line in special array
args=("$@")
#echo arguments to the shell
echo ${args[0]} ${args[1]} ${args[2]} ' -> args=("$@"); echo ${args[0]} ${args[1]} ${args[2]}'

#use $@ to print out all arguments at once
echo $@ ' -> echo $@'

# use $# variable to print out
# number of arguments passed to the bash script
echo Number of arguments passed: $# ' -> echo Number of arguments passed: $#'

echo `pwd`

directory=`pwd`
echo "cwd is " $directory

# bash check if directory exists
if [ -d $directory ]; then
	echo "Directory exists"
else 
	echo "Directory does not exists"
fi 
fname="dir/fname"
OF=$(date +%Y%m%d_%H:%M)
echo $OF

A="This is a test"
bash test2.sh "$A"