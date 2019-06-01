#!bin/bash
while :
do
    if git checkout master &&
        git fetch origin master &&
        [ `git rev-list HEAD...origin/master --count` != 0 ] &&
        git merge origin/master
    then
        echo 'Updated!'
        kill ${ps -A | grep python3 |cut -c2-5}
        python3 app.py &
	echo 'Server Started!'
    fi
    sleep 10s
done
