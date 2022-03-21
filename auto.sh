#!/bin/bash
set -e

git pull

#./check_target_link.sh
#python3 check_target_link.py
python3 download_data.py
python3 make_data.py
./update_to_github.sh
./send_email.sh
