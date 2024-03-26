sudo docker build -t pcapcopier .
sudo docker-compose -f docker-compose.yml up -d
sleep 30
sudo docker-compose -f docker-compose.yml down
sudo docker stop pcapcopier
sudo docker rm pcapcopier
sudo docker image rm pcapcopier
sudo docker image rm alpine
