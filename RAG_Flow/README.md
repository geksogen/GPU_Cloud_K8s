# Use GPU for k8s runtime

### Resource
* Ubuntu 24.04.1 с среда контейнеров Docker/NGC
* NGC Cli
* Docker 27.3.1
* nvidia-container-toolkit
* cuda-toolkit 12.6
* anaconda 24.9.2 - python 3.9
* pytorch 2.5.1 - python 3.11
* tensorflow-gpu 2.4.1
* open-driver 560
* HDD 240Gb
* RAM 16Gb
* RTX2080TI 11GB 

```Bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

```Bash
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/docker
sudo sysctl -w vm.max_map_count=262144
# elasticsearch:8.17.1
docker compose up -d
docker exec -it ollama sh
ollama pull owl/t-lite
ollama pull mxbai-embed-large
exit
```
Clear
docker-compose down --remove-orphans

Click Logo => Model providers => Add Llama = Name Model "owl/t-lite" base url "http://176.99.131.176:11434/"
# ollama pull mxbai-embed-large

docker-compose down --rmi all -v --remove-orphans
docker stop $(docker ps -a -q)
docker system prune -a
