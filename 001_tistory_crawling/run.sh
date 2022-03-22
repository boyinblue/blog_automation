#!/bin/bash
set -e

git pull

current_dir=$(pwd)

############################
# Step 1. Download Data
############################
#./check_target_link.sh
#python3 check_target_link.py
python3 download_data.py -json=tmp/list.json -csv=tmp/list.csv

############################
# Step 2. Make HTML file
############################
python3 make_data.py -input=tmp/list.json -output=tmp/list.html

pushd ..
############################
# Step 3. Update to GitHub Issue
############################
./update_to_github.sh boyinblue blog_automation 1 ${current_dir}/tmp/list.html

############################
# Step 4. Send e-mail
############################
./send_email.sh -body=${current_dir}/tmp/list.html -header=${current_dir}/email_header.txt -email=${current_dir}/tmp/email.txt
popd
