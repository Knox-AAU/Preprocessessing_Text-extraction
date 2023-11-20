# Activating and setting up virtualenv
```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

# If cool boy:
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
python3 -m pip install --editable .
```

# Docker compose commands

### Build containers
* **To build developer environment**
```bash
docker compose -f docker-compose-dev.yml build
```
* **To build production environment**
```bash
docker compose -f docker-compose-prod.yml build
```

### Start containers
* **To run developer environment**
```bash
docker compose -f docker-compose-dev up -d
```
* **To run production environment**
```bash
docker compose -f docker-compose-prod up -d
```

### Stop containers
* **To stop developer environment**
```bash
docker compose -f docker-compose-dev down
```
* **To stop production environment**
```bash
docker compose -f docker-compose-prod down
```