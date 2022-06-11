# DOCKERFILE

This `dockerfile` install the following things from apt:

- python3
- pip
- tree
- nano
- sqlite3

From requirements, if you want install something whith pip add one line with the library wanted and the version:

- pytest==7.1.1
- fastapi==0.78.0
- uvicorn==0.17.6
- black==22.3.0
- flake8==4.0.1
- isort==5.10.1
- mypy==0.961
- requests==2.28.0

#### BUILD AN IMAGE FROM A DOCKERFILE AND CREATE A CONTAINER


Build an image from a `Dockerfile` 

> Note: you must be in the same path as the `Dockerfile` at least in this command in specific

    docker build -t apirest:0.1 .

You can see if the image was created propetly with

    docker images

Now you have to create a container with the custom image that we made also a volume

    docker run -it -v $(pwd):/home/ --net=host --name apirest -h psypc apirest:0.1

You can check all your container with

    docker ps -a

you can remove a containter with

    docker rm 2cf2c92e8e2c

and for an image

    docker rmi 3da596099b8c

now if you are out from a container you can get in with 

    docker start -i apirest


If you make some changes and want to create a new image from a container you can use 

    docker commit apirest apirest:0.2  

> Note: you can use name or id instead one of them in several commands that were shown

You can consult [The official documentation of Docker](https://docs.docker.com/) if you have any question or trouble with the commands given here.