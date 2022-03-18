#!/bin/bash

cp email_header.txt tmp/email.txt
cat tmp/list.html >> tmp/email.txt
cat tmp/email.txt| ssmtp -t -v
