#!/bin/bash

# define global variables
BUILD_CLIENT=false
RUN_CLIENT=false
DEBUG=false
CLEAN_ALL=false
CLEAN_CTR=false
CLEAN_IMG=false

CTR_NAME=server_container
IMG_NAME=server_image

SERVERFILE=app/run.py
WKG_DIR="dev"
PORT=80

bold=$(tput bold)
reset=$(tput sgr0)

# define main script
main () {

    # declare variables
        # none

    # check for bad call
    check_empty "$@"

    # Iterate over arguments
    while [[ $# -gt 0 ]]; do

        # begin after 2nd arg
        case "$1" in
            -b) # build image
                BUILD_CLIENT=true
                ;;
            -r) # run image
                RUN_CLIENT=true
                ;;
            -ca) # clean all
                CLEAN_ALL=true
                ;;
            -cc) # clean containers
                CLEAN_CTR=true
                ;;
            -ci) # clear images
                CLEAN_IMG=true
                ;;
            *)
                usage
                exit 1
                ;;

        esac
        shift # Shift arguments left
    done #end while loop
    
    echo_variables

    # clean containers
    if [ $CLEAN_ALL = true ] || [ $CLEAN_CTR = true ]; then
        docker_clean_containers # clean containers
        if [ $CLEAN_CTR = true ]; then # exit only if we clear just containers
            exit 0
        fi
        
    fi

    # clean existing stuff
    if [ $CLEAN_ALL = true ] || [ $CLEAN_IMG = true ]; then
        docker_clean_images # clean images
        exit 0 # definitely exit, nothing to run
    fi

    # build the client
    if [ "$BUILD_CLIENT" = true ]; then
        docker_build
    fi 

    # run the client
    if [ $RUN_CLIENT = true ]; then
        docker_run
    fi 
    
    #docker_clean_containers
    #docker_clean_images
    exit 0
}

check_empty () 
{
    if [ $# -eq 0 ]; then
        usage
        exit 1
    fi
}

check_file ()
{
    # VULNERABILITY: CHECK IF FILE EXISTS
    if [ ! -f "$PROPERTIES_FILE" ]; then
        echo "Error: Property file '$PROPERTIES_FILE' does not exist."
        exit 1
    fi
}

docker_build ()
{
    # build
    if ! docker build --build-arg SERVERFILE=$SERVERFILE \
                      --build-arg WKG_DIR=$WKG_DIR \
                      --build-arg PORT=$PORT \
                      -t $IMG_NAME . ; then
        echo "Failed to build $IMG_NAME"
        exit 1
    fi
}

docker_clean_containers ()
{
    # Check if there are any containers to stop and remove
    if [ -n "$(docker ps -a -q)" ]; then
        echo "Stopping all running containers..."
        docker stop $(docker ps -a -q)  # Stop all containers

        echo "Removing all stopped containers..."
        docker rm $(docker ps -a -q)    # Remove all containers
    else
        echo "No containers to remove."
    fi
}

docker_clean_images ()
{
    # Check if there are any containers to stop and remove
    if [ -n "$(docker ps -a -q)" ]; then
            # Delete all images
        echo "Deleting all images..."
        docker rmi $(docker images -q)  # Delete all images
    else
        echo "No images to remove."
    fi
}


docker_run () 
{
    echo "Trying to run $bold$CTR_NAME$reset from $bold$IMG_NAME$reset..."

    docker run -it --name $CTR_NAME -p $PORT:$PORT $IMG_NAME
}

echo_variables ()
{
    echo "CTR_NAME:       $CTR_NAME"
    echo "IMG_NAME:       $IMG_NAME"
    echo "PORT:           $PORT"
}

usage () 
{
    echo "Usage: $0 [-b] [-r] [-ca] [-cc] [-ci]"
    echo "Options:"
    echo "  -b         Build image"
    echo "  -r         Run image"
    echo "  -ca        Clean all"
    echo "  -cc        Clean containers"
    echo "  -ci        Clear images"
}

# run the main script
main "$@"