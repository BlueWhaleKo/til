#!/bin/bash

set -ex

function load_br_netfilter() {
  if [[ $(lsmod | grep br_netfilter | wc -l) -eq 0 ]]; then
    sudo modprobe br_netfilter
  fi

cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF

  sudo sysctl --system
}

# install docker
function install_docker() {
  sudo apt-get update
  sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

  curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo \
    "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.doker.com/linux/ubuntu  $(lsb_release -cs) stable" \
    | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  sudo apt-get update
  sudo apt-get install -y docker-ce=18.06.2~ce~3-0~ubuntu -y

  # Create required directories
  sudo mkdir -p /etc/systemd/system/docker.service.d

  # Create daemon json config file
  sudo tee /etc/docker/daemon.json <<EOF
{
"exec-opts": ["native.cgroupdriver=systemd"],
"log-driver": "json-file",
"log-opts": {
"max-size": "100m"
},
"storage-driver": "overlay2"
}
EOF

  # Start and enable Services
  sudo systemctl daemon-reload
  sudo systemctl restart docker
  sudo systemctl enable docker

  # Add user group
  usermod add -aG docker vagrant

}

# install kubernetes
function install_kubernetes() {
  sudo apt-get update
  sudo apt-get -y install apt-transport-https ca-certificates curl
  sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
  echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

  sudo apt-get update
  sudo apt-get -y install kubelet kubeadm kubectl
  sudo apt-mark hold kubelet kubeadm kubectl
}

# [ main ]
load_br_netfilter

if [[ -x $(command -v docker) ]]; then
  install_docker
fi

if [[ -x $(command -v kubectl) ]] || [[ -x $(command -v kubeadm) ]] || [[ -x $(command -v kubelet) ]]; then
  install_kubernetesc
fi
