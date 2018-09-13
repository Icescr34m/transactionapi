# Project Description

A Python-Flask application that provides a RESTful endpoint to validade transactions, using MySQL to persist informations during execution time.


## Dependencies

- Database

```
MySQL 5.7
```


- Python Modules

* [Flask==1.0.2](http://flask.pocoo.org/docs/1.0/changelog/) - Microframework WEB
* [Flask-SQLAlchemy==2.3.2](http://flask-sqlalchemy.readthedocs.io/en/stable/) - ORM Toolkit
* [PyMySQL==0.9.1](https://pypi.org/project/PyMySQL/) - MySQL Connector

```
Docker and docker-compose (Latest)
```

## API Endpoint

You can find the API endpoint in:

```
/api/v1.0/validate/transaction
```

## Template request used to test the application (JSON)

```
{
	"Account": [{
		"cardIsActive": "True",
		"limit": 920,
		"blacklist": ["Fatura Aberta"],
		"isWhitelisted": "True"
	}],
	"Transaction": [{
		"merchant": "Carrefour",
		"amount": 200,
		"time": "15-Dezembro-2012"
	}],
	"LastTransactions": [{
		"Transactions": [200, 300, 600]
	}]
}
```

## Container structure

```
- CentOS 7 Container with Python3.6 running the entire Python-Flask application.
```

```
- Container MySQL running the validator database, already with the tables.
```

## Environment Configuration

If you're running the Docker stack (Python + MySQL) in a CentOS 7 VM (Recommended) some configurations are necessary:

- Linux Kernel (sysctl.conf):

```
Add net.ipv4.ip_forward = 1 in /etc/sysctl.conf to allow docker containers use internet from host.
```


- Network Ports:

```
The APP and Database consume ports: 5000 and 3306 (TCP)
```

- Environment.sh script:

```
Need to provide execution permission in the script Environment.sh. Ex: chmod +x Environment.sh
```

- SELinux and IPtables:

```
If Running externally, need to configure IPtales and SELinux to accept and allow I/O traffic to the specified ports.
```

- MySQL Client:

```
Need a MySQL client installed in the host that will run the container, used for configuration purposes.
```

- Git

```
Need a Git package installed.
```

## Installing the Application Stack

To install the application, you need to have up and running Docker and docker-compose.
If you have passed for the Environment configuration, you just need to enter in the project directory and run: ./Environment.sh.

## Unit Tests

```
NEED TO KNOW:

The function test_more_than_ten use ten post requests to validate if after ten transactions with the same merchant he will be blocked and invalidate next transactions.

If you need to run the unit tests more than one time you have two options:

I) Restart the entire environment (docker-compose down; ./Environment.sh) and then run again.
II) Change the merchant value in the dictionary data_post in the function test_more_than_ten
```

```
The Unit tests are included in the Docker Python-Flask container, to run the tests you have two options:
I) Execute the tests inside the Docker container:
    1) docker exec -it python-flask-app bash
    2) python3.6 test_api.py -v

II) Execute the tests out of the container:
    docker exec python-flask-app python3.6 test_api.py -v
```

All the test functions are commented to provide a better understanding of what is going on.

## Test the API usability via CLI:

cURL Example:

```
curl -XPOST -H "Content-type: application/json" -d '{ "Account": [{ "cardIsActive": "True", "limit": 9200, "blacklist": ["BadPay", "Hooka"], "isWhitelisted": "True" }], "Transaction": [{ "merchant": "renato", "amount": 500, "time": "15-Dezembro-2012" }], "LastTransactions": [{ "Transactions": [200, 300, 600] }] }' 'http://192.168.0.12:5000/api/v1.0/validate/transaction'
```

PS: The application works with RAW type in the BODY of the requisition.


## Plus Environment

For agility purposes, i've setted a CentOS 7 Virtual Machine with all the Environment Requirements done, just needing to install and use the application.

Informations to access the pre-configured environemnt.

```
IP: 35.231.83.130
```

```
User: validator
```

```
Password: BHU*nji9
```

```
SSH Port: 22
```

```
Gain ROOT Permission: sudo su
```

If you run the application in this Virutal Machine, the API will be exposed externally and can be accessed normally.
EX:

```
curl -XPOST -H "Content-type: application/json" -d '{ "Account": [{ "cardIsActive": "True", "limit": 9200, "blacklist": ["BadPay", "Hooka"], "isWhitelisted": "True" }], "Transaction": [{ "merchant": "renato", "amount": 500, "time": "15-Dezembro-2012" }], "LastTransactions": [{ "Transactions": [200, 300, 600] }] }' 'http://35.231.83.130:5000/api/v1.0/validate/transaction'
```









