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