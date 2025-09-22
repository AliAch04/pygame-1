import os
if 'VIRTUAL_ENV' in os.environ:
    print("Inside venv")
else:
    print("Not in venv")