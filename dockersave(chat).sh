#! /bin/bash
#Script for save container docker(Chat)
fechaservices=$(date +'%d_%m_%Y_%T')
fecha=$(date +'%d_%m_%Y')
fecharecup=$(date +'%d_%m_%Y' --date="2 day ago")
rest(){
    echo "Restore containers..."
    cd /root/ || return
    echo "Compose down containers..."
    docker-compose down
    cd /root/$fecharecup || return
    echo "Restoring containers..."
    for i in $(ls | grep .tar)
        do
            docker load -i $i
            echo "Restore container:$1"
        done
    cp -r /root/$fecharecup/db /root/data/db
    cd /root/ || return
    echo "Starting services..."
    docker-compose up -d
}    
if [ "$1" = "save" ]
then
    echo "Creating folder..."
    mkdir $fecha
    cd $fecha || return
    echo "Saving containers..."
    for i in $(docker ps --format {{.Image}})
    do
        save="$i"
        arr=($(echo $save | tr "/" "\n"))   
        docker save -o ${arr[0]}.tar $i
        echo "Sucefully container save:$i with date: $fechaservices"
    done
    echo "Saving Database..."
    cp -r /root/data/db /root/$fecha
fi
if [ "$1" = "restore" ]
then
    rest
fi
if [ "$1" = "check" ]
then
    echo "Checking services..."
    for i in $(docker ps --format {{.ID}})
    do
        RUNNING=$(docker inspect --format="{{.State.Running}}" $i)
        if [ "$RUNNING" == "true" ]; then
            echo -e "Container $i is alive with date:$fechaservices"
        elif [ $RUNNING != "true" ]; then
             echo -e "Container $1 is down with date:$fechaservices"
             rest
             break
        else
            echo -e "Container not exist"
        fi
    done
fi