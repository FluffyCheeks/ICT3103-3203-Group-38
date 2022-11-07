# ICT3103-3203-Group-38

## Pre-Installation for the project

1. Git clone the project from this repository(https://github.com/asdwty/ICT3103-3203-Group-38)
``` 
https://github.com/asdwty/ICT3103-3203-Group-38.git
```

2. Follow these steps to help preinstall required modules
```
cd pastelLuna #enter the file directory
py -m venv .venv #create a virtual environment
.venv/scripts/activate #activate the virtual environment
```
3. Enter these pip commands to install required packages
```
cd .. #exit the pastelluna to install requirements
pip install -r requirements.txt

# for static images
python manage.py collectstatic
```

Note. Gmail only have a limit of 100 message per day. So if you get server500 it is because limit is reached. 
Need to wait for suspension period to resume, then sending mail will work 
https://support.google.com/a/answer/166852?hl=en
