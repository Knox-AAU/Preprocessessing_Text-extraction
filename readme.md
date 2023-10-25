# Activating and setting up virtualenv
```bash
virtualenv .env && source .venv/bin/activate && pip install -r requirements.txt
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