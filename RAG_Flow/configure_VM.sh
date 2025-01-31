sudo apt update
sudo curl -L "https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/docker
sudo sysctl -w vm.max_map_count=262144
rm -rf docker-compose-base.yml
curl -o docker-compose-base.yml https://raw.githubusercontent.com/geksogen/GPU_Cloud_K8s/refs/heads/master/RAG_Flow/docker-compose.yml
sudo docker compose up -d
docker exec -it ollama sh
