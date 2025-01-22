sudo apt update
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
git clone https://github.com/geksogen/GPU_Cloud_K8s.git
cd Llama_webUI_chat
docker-compose up -d
