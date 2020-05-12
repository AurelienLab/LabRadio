**Installation**

Install dependencies

```
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install -y python3-pyqt5 python3-pyaudio portaudio19-dev
sudo apt-get -y install python3-gst-1.0 gstreamer1.0-plugins-ugly gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-alsa python-gobject python3-redis redis-server python3-pip
```

Configure redis for openob

```
sudo sed -i.bak 's/bind 127.*/bind 0.0.0.0/' /etc/redis/redis.conf && sudo service redis-server restart
```

Clone repository

```
git clone https://github.com/AurelienLab/LabRadio.git
```

Install requirements
```
pip3 install -r LabRadio/requirement.txt
```

Start program
```
python3 LabRadio/main.py
```