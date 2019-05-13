# Usage
# Intialize environment

## Global VENV initialization

    sudo apt install -y python3-pip
    sudo apt install build-essential libssl-dev libffi-dev python3-dev
    sudo apt install -y python3-venv

    mkdir crawler
    cd crawler/
    python3.6 -m venv venv
    source venv/bin/activate
    
    git clone https://github.com/FremanZhang/shelob.git
    pip install -r shelob/src/requirements.txt
    cd shelob/
    git pull

## Create amap key file

    mkdir ./pri
    echo 'Your amap web serivce key' > ./pri/amap_ws.key

## Create amap navigationAreaRoute HTML doc
    
    touch ./pri/navigationAreaRoute.html
