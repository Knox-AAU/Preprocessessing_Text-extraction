# Activating and setting up virtualenv
```bash
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
```

# To lint code
1) Be in folder with files you want to lint (usually root)
2) 
```bash
pylint *.py
```