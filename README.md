#APOF

## Instalation

[Install Docker](https://docs.docker.com/engine/installation/linux/ubuntulinux/)
[Install Compose](https://docs.docker.com/compose/install/)
Clone this repo
```
cd /your/dev/path/
git clone git@github.com:PyPila/apof.git
cd apof
```
Provision MySQL 
```
docker-compose up -d db
```

## Work instance
```
docker-compose up 
```
Considering you don't have anything running on ports `80` and `8000` you should be able to access your development instance by http://127.0.0.1/. If you have those ports used consider changing `docker-compose-yml` and `nginx/apof.conf`.
