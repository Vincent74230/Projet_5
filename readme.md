# 'Pur-beurre' application
## This programm offers healthier alternatives to what you usually eat
---
### How to install this programm (GNU/LINUX : ubuntu)

__You must have a SQL server installed on your system.__

If not, follow the whole path.
If so, skip step 1.

#### Step 1 (mysql installation)

In your console, type:

    sudo apt-get install mysql-server mysql-client

You can change your root password if U want, with this line:

    sudo mysqladmin -u root -h localhost password your_password

#### Step 2 (required modules installation)

In your console, type:

    pip3 install -r requirements.txt

#### Step 3 (Create a user)

Log into mysql as root:

    sudo mysql -u root -p

Type those lines into mysql 

    CREATE USER 'oc_student'@'localhost' IDENTIFIED BY 'password';

    GRANT ALL PRIVILEGES ON pur_beurre.* TO 'oc_student'@'localhost';

Exit mysql by typing 'exit'

#### Step 4 (app installation)

In your console type (or copy paste):

    python3 init.py

#### Step 5 (run it)

Type:

    python3 main.py

Follow instructions on the screen
