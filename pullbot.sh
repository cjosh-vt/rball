#!/bin/bash
while :
do
    if git checkout master &&
        git fetch origin master &&
        [ `git rev-list HEAD...origin/master --count` != 0 ] &&
        git merge origin/master
    then
        echo 'Updated!'
        ps -ef | grep -i python3 | grep -i app.py| awk '{kill $2}'
        python3 app.py &
	echo 'Server Started!'
    fi
    sleep 10s
done
