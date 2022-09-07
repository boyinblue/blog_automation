#!/bin/bash
set -e -x

TEMP_FILE=$(tempfile)

function print_usage()
{
  set +x
  echo "Send e-mail"
  echo "(Usage) ${0} -body=(content file path) -header=(email_header) -email=(whole email path)"
  echo "(Example) ${0} -body=tmp/list.html -header=tmp/email_header.txt -email=tmp/email.txt"
}

for i in "$@"
do
  case $i in
    -body=*)
	  BODY_PATH=${i##*=}
	  shift
	  ;;
	-header=*)
	  EMAIL_MSG_HEADER=${i##*=}
	  shift
	  ;;
	-email=*)
	  PREV_EMAIL_PATH=${i##*=}
	  shift
	  ;;
	*)
	  print_usage
	  exit
	  shift
	  ;;
  esac
done

if [ "${BODY_PATH}" == "" ]; then
  echo "There is no e-mail body path"
  print_usage
  exit 1
elif [ "${EMAIL_MSG_HEADER}" == "" ]; then
  echo "There is no e-mail header path"
  print_usage
  exit 2
fi

cp ${EMAIL_MSG_HEADER} ${TEMP_FILE}
cat ${BODY_PATH} >> ${TEMP_FILE}

if [ "{PREV_EMAIL_PATH}" == "" ] && [ -e ${PREV_EMAIL_PATH} ]; then
  diff=$(diff $PREV_EMAIL_PATH $TEMP_FILE)
else
  diff="First Send"
fi

if [ "${diff}" == "" ]; then
  echo "No need to send email"
else
  echo "Need to send email"
  cat ${TEMP_FILE} | ssmtp -t -v
  if [ "${PREV_EMAIL_PATH}" != "" ]; then
    cp ${TEMP_FILE} ${PREV_EMAIL_PATH}
  fi
fi
