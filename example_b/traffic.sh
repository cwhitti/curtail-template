#!/bin/bash

# Use this to simulate traffic by connecting to the server, either by implementing a custom client or
# just simple curl commands. This file is not required but can help automate the process of 
# sending traffic.

# example command:
# curl -X POST -d "Type_1=Water&ID=67" 0:80/search

TYPES=("Bug" "Dragon" "Electric" "Fighting" "Fire" "Flying" "Ghost" "Grass" "Ground" "Ice" "Normal" "Poison" "Psychic" "Rock" "Water")
SERVER="127.0.0.1:8009"
ENDPOINT="search"
TRAFFIC=25

function main() {
    # Loop to generate traffic
    for (( i=0; i<TRAFFIC; i++ )); do
        data=""
        #attack=$(( RANDOM % 2 ))
        type_1=$(( RANDOM % 2 ))
        type_2=$(( RANDOM % 2 ))
        attack=0
        # type_1=1
        # type_2=0

        # Non-attacking code, construct normal data
        if [ $attack -eq 0 ]; then

            ATTACK_TYPE="REGULAR"

            if [ $type_1 -eq 1 ]; then
                data+="Type_1=$(random_type)"

                if [ $type_2 -eq 1 ]; then
                    data+="&"
                fi
            fi

            if [ $type_2 -eq 1 ]; then
                data+="Type_2=$(random_type)"
            fi

        # SQL attack mode, construct malicious data
        else
            ATTACK_TYPE="ATTACK!"
            if [ $type_1 -eq 1 ]; then
                data+='Type_1=Water"; DROP TABLE pkmon_tbl; --'

                if [ $type_2 -eq 1 ]; then
                    data+="&"
                fi
            fi

            if [ $type_2 -eq 1 ]; then
                data+='Type_2=Water"; DROP TABLE pkmon_tbl; -- '
            fi
        fi

        endline
        endline
        endline

        echo "($ATTACK_TYPE) curl -X POST -d $data $SERVER/$ENDPOINT (!)"
        endline


        curl -X POST -d "$data" "$SERVER/$ENDPOINT"
    done
}


function random_type ()
{
    NUM_TYPES=${#TYPES[@]}

    # gen random index
    INDEX=$(( RANDOM % NUM_TYPES ))

    # get random type
    RANDOM_TYPE=${TYPES[INDEX]}

    echo $RANDOM_TYPE
}

function endline ()
{
    echo ""
}

main