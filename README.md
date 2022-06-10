# API-REST

docker build -t apirest:0.1 .

docker run -it -v /workspace/API-REST/:/home/ --net=host --name apirest -h psypc apirest:0.1