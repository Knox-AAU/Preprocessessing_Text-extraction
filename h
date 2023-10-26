""" Helper tool for improved programming experience """

import os
import sys

if sys.argv[1] == 'lint'.lower():
    os.system('pylint ./**/*.py')

elif sys.argv[1].lower() == 'test':
    os.system("python -m unittest discover -s src -p 'test_*.py'")

else:
    print(f"Invalid command: {sys.argv[0]} - valid commands are: test & lint")
