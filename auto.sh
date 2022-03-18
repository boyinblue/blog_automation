#!/bin/bash

git pull

#./check_target_link.sh
python3 check_target_link.py
./update_to_github.sh
./send_email.sh
