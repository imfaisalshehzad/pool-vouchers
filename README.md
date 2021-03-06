# Setup

## Docker setup

### Clone your repo

    $ git clone https://github.com/imfaisalshehzad/pool-vouchers.git

### Make sure docker is installed on your system and run following commands inside your project directory:

    $ docker-compose build
    $ docker-compose up

### Execute the below commands to setup project db and super admin:

    $ make makemigrations
    $ make migrate
    $ make install-package
    $ make createsuperuser

## Development Steps

1. Install <b>git</b> on the system.
2. Open shell/command prompt and run following command to clone the project:
   <br>`$ git clone https://github.com/imfaisalshehzad/pool-vouchers.git`


3. Make sure <b>python3</b> and <b>pip3</b> are installed on the system.
4. Once inside the project's root directory, install requirements using the following command:
   <br>Note: It's recommended to create a virtual environment and install requirements there.
   <br>`$ pip install -r ./requirements/local.txt`

5. Run this command inside the project directory to start the server:
   <br>`$ python3 manage.py runserver 8000`
   
   
### Create Dummy Data

You can create dummy data by running the mentioned below command.

    $ make sample-data

### Django Admin Panel URL:
User your login details that you have create for the super admin.

    $ http://127.0.0.1:8000/admin/


### Admin Panel Generate Vouchers
You can also create vouchers via admin panel dashboard.

   ![alt text](https://i.imgur.com/T81LMPv.png)


### Interact with APIs on this URL:
You can access the APIs details on:

    $ http://127.0.0.1:8000/collection/schema/swagger/


### Testcase:
Run test by using the below command in terminal.

    $ make run-test


