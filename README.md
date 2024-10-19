# luces_maqueta

Creacion del entorno virtual 
python -m venv venv
pip install -r requirements.txt

Activacion del entorno virtual
venv/bin/activate

chmod u+x app.py

Inicio automatico

sudo crontab -e
@reboot /bin/bash -c 'source /home/911exp/luces_maqueta/venv/bin/activate && python /home/911exp/luces_maqueta/app.py >> /home/911exp/luces_maqueta/log.txt 2>&1'

nmcli connection show
nmcli connection show "preconfigured"

sudo nmcli connection down "preconfigured"
sudo nmcli connection up "preconfigured"

sudo nmcli connection modify "preconfigured" ipv4.addresses 10.1.1.10/24
sudo nmcli connection modify "preconfigured" ipv4.gateway 10.1.1.1
sudo nmcli connection modify "preconfigured" ipv4.dns 10.1.1.1
sudo nmcli connection modify "preconfigured" ipv4.method manual