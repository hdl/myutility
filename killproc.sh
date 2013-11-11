for i in `seq $1 $2`;
do
	kill $i
	echo "process $i killed"
done
ps -auxww | grep zemao
exit 0
