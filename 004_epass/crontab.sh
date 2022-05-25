#!/bin/bash

git pull
./auto.sh
./update_event2.py -host=mesti -op=add -dir=tmp
