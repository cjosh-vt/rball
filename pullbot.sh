#!/bin/bash
APP_CODE=$(ps -ef | grep -i python3 | grep -i app.py)
if [ -z "$APP_CODE" ]
then
    python3 app.py &
fi
while :
do
    if git checkout master &&
        git fetch origin master &&
        [ `git rev-list HEAD...origin/master --count` != 0 ] &&
        git merge origin/master
    then
        echo 'Updated!'
        APP_CODE=$(ps -ef | grep -i python3 | grep -i app.py)
        if [ -z "$APP_CODE" ]
        then
            echo{"$APP_CODE"} | awk '{kill $2}'
            sleep 5s
            python3 app.py & #>log.txt 2>error.txt&
	    echo 'Server Started!'
        fi
    fi
    sleep 10s
done
