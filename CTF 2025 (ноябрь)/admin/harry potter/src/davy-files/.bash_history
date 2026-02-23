ls -la
cd webserver
python3 -m venv .venv
source .venv/bin/activate
pip install flask
cat password.txt
cat password.txt > joey_ssh_creds.txt
rm joey_ssh_creds.txt
python main.py
