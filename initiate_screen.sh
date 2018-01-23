#!/bin/bash
##################################Initiate Screen####################################
#name of the screen
PROJECT_NAME=$1
#name of the screen inside the project screen
DESCRIPTOR=$2
#Json config file with web socket information
PORT=$3
VIRTUAL_ENV_NAME=$4
WEB_STREAM_PORT=$5
WEB_SECRET=$6

if [  -z "$PROJECT_NAME" ]
    then
    echo "PROJECT_NAME is empty";
    exit 1;
fi

if [  -z "$DESCRIPTOR" ]
    then
    echo "DESCRIPTOR is empty";
    exit 1;
fi

if [  -z "$VIRTUAL_ENV_NAME" ]
    then
    echo "VIRTUAL_ENV_NAME is empty";
    exit 1;
fi

echo "creating screen for project ${PROJECT_NAME}, descriptor ${DESCRIPTOR}"
#Check if project exists before initializing it again
if ! screen -list | grep -q $PROJECT_NAME; then
    screen -AdmS $PROJECT_NAME -t "${DESCRIPTOR} \n"
else
    echo "project name already exists";
    exit 1;
fi
#create the screen can run start the web socket relay
screen -S $PROJECT_NAME -t $DESCRIPTOR -X stuff "workon ${VIRTUAL_ENV_NAME} \n";
screen -S $PROJECT_NAME -t $DESCRIPTOR -X stuff "python web_socket_relay.py ${PORT} ${WEB_STREAM_PORT} ${WEB_SECRET} \n";


