# PROG8850Template
Environment with MySQL, Python, Node and Docker.

## Quick start
```bash
pip install -r requirements.txt
ansible-playbook up.yaml
pytest dbtests.py
```
When you are done working with the database run:
```bash
ansible-playbook down.yaml
```

To access database manually:
```bash
sudo mysql -u root
```

Happy MySQL!
