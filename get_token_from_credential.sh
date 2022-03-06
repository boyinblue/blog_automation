#!/bin/bash

credential=$(cat ~/.git-credentials)
credential=${credential##https://}
credential=${credential%%@*}

id=${credential%%:*}
token=${credential##*:}

echo "ID : ${id}"
echo "token : ${token}"
