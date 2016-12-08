import os
from shutil import rmtree

print('Removing temporary directory')

# check for the tmp directory and remove it
if os.path.isdir('./app/tmp'):
    rmtree('./app/tmp')

print('Temporary directory removed')

# ask the user if they want to keep the results.jpg file, if not remove
answer = input('Would you like to keep the results file? (y/n)')
if answer.lower() == 'n':
    os.remove('./results.jpg')
    print('\'results.jpg\' has been removed.')
else:
    print('\'results.jpg\' has not been removed.')

