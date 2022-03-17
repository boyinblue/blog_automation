#!/bin/bash

git pull

#./check_target_link.sh
python3 check_target_link.sh
./update_to_github.sh
