## Reinstall Nvidia Driver && Install CUDA 9.0 , CuDNN 7.0.5

### Uninstall Nvidia Driver

Remove Nvidia Nouveau Driver 
```
$ sudo bash -c "echo blacklist nouveau > /etc/modprobe.d/blacklist-nvidia-nouveau.conf"
$ sudo bash -c "echo options nouveau modeset=0 >> /etc/modprobe.d/blacklist-nvidia-nouveau.conf"
```

Confirm the content of the new modprobe config file
```
$ cat /etc/modprobe.d/blacklist-nvidia-nouveau.conf
[blacklist nouveau options nouveau modeset=0]
```


Update kernel initramfs
```
$ sudo update-initramfs -u
$ sudo reboot
```

Remove Any Other NVIDIA Driver && Add the graphics driver PPA
```
$ sudo apt-get purge nvidia*
\\sudo apt remove --purge -s nvidia-*
\\sudo apt remove --purge -s libnvidia-*
\\sudo apt autoremove
$ sudo reboot

```

Install NVIDIA Driver
```
$ sudo apt update
$ sudo add-apt-repository ppa:graphics-drivers/ppa
$ sudo apt update
$ sudo apt install nvidia-driver-390 | 410 | 450
```

### Install CUDA 9.0

download : https://drive.google.com/file/d/1cmHoAhMPHdUN3x87bDZx0-YKgkkiNuxS/view?usp=sharing
```
$ sudo dpkg -i cuda-repo-ubuntu1704-9-0-local_9.0.176-1_amd64.deb
$ sudo apt-key add /var/cuda-repo-9-0-local/7fa2af80.pub
$ sudo apt-get update
$ sudo apt-get install cuda=9.0.176-1
```

```
$ sudo nano ~/.bashrc

# CUDA 9.0
export CUDA_HOME=/usr/local/cuda
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
# END CUDA 9.0

$ source ~/.bashrc
$ nvcc -V
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2017 NVIDIA Corporation
Built on Fri_Sep__1_21:08:03_CDT_2017
Cuda compilation tools, release 9.0, V9.0.176
```

### Install CuDNN 7.0.5

download : https://drive.google.com/file/d/1cmHoAhMPHdUN3x87bDZx0-YKgkkiNuxS/view?usp=sharing
```
$ tar -xzvf cudnn-9.0-linux-x64-v7.tgz
$ cd cudnn-9.0-linux-x64-v7
$ sudo cp cuda/include/cudnn.h /usr/local/cuda/include
$ sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
$ sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
```