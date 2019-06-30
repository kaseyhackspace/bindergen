source /home/pi/env/bin/activate
cd /home/ubuntu/bindergen
gunicorn -w 4 -b 0.0.0.0:8000 app:app
