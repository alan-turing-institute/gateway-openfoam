#!/bin/bash

# based on
# https://hharnisc.github.io/2016/06/19/integration-testing-with-docker-compose.html

# define some colors to use for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
# kill and remove any running containers
cleanup () {
  docker-compose -p simulate-test kill
  docker-compose -p simulate-test rm -f
}
# catch unexpected failures, do cleanup and output an error message
trap 'cleanup ; printf "${RED}Tests Failed For Unexpected Reasons${NC}\n"'\
  HUP INT QUIT PIPE TERM
# build and run the composed services
# docker-compose -p simulate-test build && \
docker-compose -p simulate-test up -d

if [ $? -ne 0 ] ; then
  printf "${RED}Docker Compose Failed${NC}\n"
  exit -1
fi

# wait for the test service to complete and grab the exit code
TEST_EXIT_CODE=$(docker wait test)

# output the logs for the test (for clarity)
docker-compose -p simulate-test logs test

# inspect the output of the test and display respective message
if [ -z ${TEST_EXIT_CODE+x} ] || [ "$TEST_EXIT_CODE" -ne 0 ] ; then
  printf "${RED}Tests Failed${NC} - Exit Code: $TEST_EXIT_CODE\n"
else
  printf "${GREEN}Tests Passed${NC}\n"
fi

# call the cleanup fuction
# cleanup

# exit the script with the same code as the test service code
exit $TEST_EXIT_CODE
