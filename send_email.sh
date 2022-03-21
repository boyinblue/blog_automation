#!/bin/bash

PREV_EMAIL_MSG=tmp/email_prev.txt
EMAIL_MSG=tmp/email.txt
EMAIL_MSG_HEADER=email_header.txt

cp ${EMAIL_MSG_HEADER} ${EMAIL_MSG}
cat tmp/list.html >> ${EMAIL_MSG}

if [ -e ${PREV_EMAIL_MSG} ]; then
  diff=$(diff $PREV_EMAIL_MSG $EMAIL_MSG)
else
  diff="First Send"
fi

if [ "${diff}" == "" ]; then
  echo "No need to send email"
else
  echo "Need to send email"
  cat ${EMAIL_MSG} | ssmtp -t -v
  cp ${EMAIL_MSG} ${PREV_EMAIL_MSG}
fi
