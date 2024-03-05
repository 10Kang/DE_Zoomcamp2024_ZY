## Installation of Docker in Google Cloud Compute (Ubuntu)

After the installation of docker engine for ubuntu followed the steps by docker documentation [here](https://docs.docker.com/engine/install/ubuntu/). To avoid using the `sudo` command for each docker operation, we can run the command below and relaunched the compute enginer accordingly


```
$ sudo groupadd docker
$ sudo gpasswd -a $USER docker
```

## Run the data orchestration tool: MAGE in docker

1. To set up Mage in docker with pyspark, make sure the `Dockerfile` is with command to download `java` and also `pyspark` module from the `requirements.txt`. Check out the [Dockerfile](./Dockerfile).  
   
2. Rename the `dev.env` to `.env` to make sure the docker file can access the variable in the environment. The `.env` file will store the name of your project for Mage.
  
```{bash}
$ mv dev.env .env
```
3. Run `docker compose up` to run the command defined in the `docker-compose.yml`. Remember to map the port for application you wish to access its UI to the port of virtual machine. Example, MAGE at port:6789 and Spark UI at port:4040.

```{bash}
$ docker compose up -d
```

4. You might wonder why running pyspark in the local compute engine. It probably will crash the machine if the data size get larger. However, the data in this portfolio is small and for practice purpose, thus running in local mode, rather than the cluster mode like in EMR or dataproc.