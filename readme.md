# Activating and setting up virtualenv
```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

# Helper functions (h file):
To lint: 
```bash
python h lint
```
To test: 
```bash
python h test
```

# To lint code
1) Be in folder with files you want to lint (usually root)
2) 
```bash
pylint ./**/*.py
```

# To run tests
1) Be in root folder 
2) 
```bash
python -m unittest discover -s src -p 'test_*.py'
```

# Command to setup setuptools and fix imports etc
```bash
python -m pip install --editable .
```

# Docker compose commands
*Sudo rights may be needed - use: " **sudo {command you want to run}** "*
### Build containers
* **To build developer environment**
```bash
docker compose -f docker-compose-dev.yml build
```
* **To pull production environment**
```bash
docker compose -f docker-compose-prod.yml pull
```

### Start containers
* **To run developer environment**
```bash
docker compose -f docker-compose-dev.yml up -d
```
* **To run production environment**
```bash
docker compose -f docker-compose-prod.yml up -d
```

### Stop containers
* **To stop developer environment**
```bash
docker compose -f docker-compose-dev.yml down
```
* **To stop production environment**
```bash
docker compose -f docker-compose-prod.yml down
```