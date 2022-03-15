#!/bin/bash

# SO:12264238 as inspiration
# add -r to inotifywait command if you want to check folders recursively

if ! hash inotifywait  &> /dev/null
then
  apt -y -qq update && apt -qq -y install inotify-tools
fi
 

sigint_handler()
{
  [[ $(jobs -pr) == "" ]] || kill $(jobs -pr)
  exit
}

trap sigint_handler SIGINT

while true; do
  $* &
  PID=$!
  inotifywait -q -e modify -e move -e create -e delete -e attrib `pwd`
  [[ $(jobs -pr) == "" ]] || kill $(jobs -pr)
  kill $PID
  echo "Restarting API (5s delay)"
  sleep 5
done