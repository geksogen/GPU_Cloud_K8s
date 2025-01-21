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
* HDD 160Gb
* RTX2080TI 11GB 

```Bash
watch -n 1 nvidia-smi # Check Nvidia card
sudo apt update
sudo apt install -y curl && curl https://get.docker.com -o install.sh && sh install.sh
sudo apt install python3-pip
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

```Bash
git clone https://github.com/geksogen/GPU_Cloud_K8s.git
cd GPU_Cloud_K8s
docker-compose up -d
docker exec -it ollama sh
ollama pull owl/t-lite
# <IP:8080> Final service
```
