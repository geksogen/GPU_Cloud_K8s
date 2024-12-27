# Use GPU for Docker runtime

### Resource
* Ubuntu v24.04
* CUDA 12.9
* CudNN 9.5
* HDD 300Gb
* RTX2080TI 11GB 

### Install Requirements
```Bash
watch -n 1 nvidia-smi # Check Nvidia card
sudo apt update
sudo apt install -y curl && curl https://get.docker.com -o install.sh && sh install.sh
sudo apt install python3-pip
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-5 # Install cuda-toolkit-12-5
# Install Nvidia Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```
### Configure Docker runtime
```Bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
cat /etc/docker/daemon.json # Check GPU Docker runtime
```
### Run Docker image for use GPU
```Bash
docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi

+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.35.03              Driver Version: 560.35.03      CUDA Version: 12.6     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 2080 Ti     Off |   00000000:05:00.0 Off |                  N/A |
|  0%   34C    P8              2W /  250W |       2MiB /  11264MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
# Its good:!
```
### Run Docker-compose service for use GPU
```Yaml
version: '3.8'

services:
  your_service_name:
    build: .
    runtime: nvidia # Activ GPU
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility
    volumes:
      - .:/app
    command: ["python", "your_script.py"]
```
### Run Python for GPU info
```Bash
pip3 install tensorflow --break-system-packages
pip3 install numpy --break-system-packages
pip3 install pandas matplotlib --break-system-packages
python3 GPU_info.py
```

### Run local Ollama server
```Bash
docker run --runtime=nvidia --gpus all -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### Links referal
[Kubernetes with GPU for MLOps Workloads](https://sivanaikk0903.medium.com/kubernetes-with-gpu-for-mlops-workloads-c684f8c8d41c)
