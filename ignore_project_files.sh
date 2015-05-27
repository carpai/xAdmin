#!/usr/bin/sh

for f in `find .idea -type f`;do 
	echo "ignore changes of idea project file: <$f>"
	git update-index --assume-unchanged $f
done
