# GET STARTED
## Requirement
* **WSL**
* **Python 3.11+**
* **Docker**

## Build the project
1) `Enter WSL (Windows ONLY)`
    * Open terminal -> type `WSL` -> Hit Enter -> type `cd` -> Hit Enter
2) `git clone git@github.com:Knox-AAU/Preprocessessing_Text-extraction.git`
3) `cd Preprocessessing_Text-extraction`
4) `source run setup`

## How to start dev environment
```bash
sh run dev up
```

## How to stop dev environment
```bash
sh run dev down
```

## How to lint project
```bash
sh run lint
```

## How to run project tests
```bash
sh run test
```

## How to run prod environment (SERVER ONLY)
```bash
sh run prod up
```

## How to stop prod environment (SERVER ONLY)
```bash
sh run prod down
```

## How to contribute
* **Branching**
* **Pull_requests**
* **Workflow**

## Deployment
* **How to deploy new version**
* **How to tag production**

# Advanced/Detailed commands for project
## Activating and setting up virtualenv
```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

## To lint code
1) Be in folder with files you want to lint (usually root)
2) 
```bash
pylint ./**/*.py
```

## To run tests
1) Be in root folder 
2) 
```bash
python -m unittest discover -s src -p 'test_*.py'
```

## Command to setup setuptools and fix imports etc
```bash
python -m pip install --editable .
```

## Docker compose commands
*Sudo rights may be needed - use: " **sudo {command you want to run}** "*
#### Build containers
* **To build developer environment**
```bash
docker compose -f docker-compose-dev.yml build
```
* **To pull production environment**
```bash
docker compose -f docker-compose-prod.yml pull
```

#### Start containers
* **To run developer environment**
```bash
docker compose -f docker-compose-dev.yml up -d
```
* **To run production environment**
```bash
docker compose -f docker-compose-prod.yml up -d
```

#### Stop containers
* **To stop developer environment**
```bash
docker compose -f docker-compose-dev.yml down
```
* **To stop production environment**
```bash
docker compose -f docker-compose-prod.yml down
```