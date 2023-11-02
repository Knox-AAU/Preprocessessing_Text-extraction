""" Helper tool for improved programming experience """

import os
import sys

if sys.argv[1].lower() == 'lint':
    os.system('pylint ./**/*.py')

elif sys.argv[1].lower() == 'test':
    os.system("python -m unittest discover -s src -p 'test_*.py' -v")

elif sys.argv[1].lower() == 'integration':
    os.system("python -m unittest discover -s src -p 'integration_*.py'")

else:
    print(f"Invalid command: {sys.argv[1]} - valid commands are: test & lint")
