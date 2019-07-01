 # Bindergen
A REST API utilising Binderhub's API Endpoint for creating binder environments

## Setup
1. `git clone https://github.com/kaseyhackspace/bindergen`
2. `cd bindergen`
3. `sudo apt update`
4. `sudo apt install python-pip python-virtualenv`
5. `virtualenv -ppython3 env`
6. `source env/bin/activate`
7. `pip install -r requirements.txt`
8. `sudo cp bindergen.service /etc/systemd/system`
9. 