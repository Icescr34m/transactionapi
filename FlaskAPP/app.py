from flask import Flask, request, flash, jsonify, session, make_response
import json
from flask_sqlalchemy import SQLAlchemy
import pymysql



# Flask Instance, Database connection Engine and some vars.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:BHU*nji9@192.168.0.11/validator'
db = SQLAlchemy(app)
transactionAmount = 0





################################  Database Tables  ################################


#Implements an ORM Object called merchant that contains values: Transaction Amount, Blacklisted or not and his name.
class merchant(db.Model):
    __tablename__ = 'merchant'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)
    isBlakcListed = db.Column('isBlackListed', db.Boolean)
    transactionAmount = db.Column('transactionAmount', db.Integer)

    def __init__(self, id, name, isBlakcListed, transactionAmount):
        self.id = id
        self.name = name
        self.isBlakcListed = isBlakcListed
        self.transactionAmount = transactionAmount



##############################  //Database Tables//  ##############################


#Function to validate transaction using ["Transaction Amount", "Last All Transactions Value", "Limit"] values. (1)
def funcValidateTransaction(amount,limit,lastAllTransactionsAmount):
    return ((int(amount)) + int(lastAllTransactionsAmount)) > int(limit)

#Function to check if card is blocked (2)
def funcCardIsActive(cardIsActive):
    return cardIsActive == "False"

#Check if first transaction is above of 90% of the limit (3)
def funcCheckFirstTransaction(amount, limit, transactionAmount):
    return (int(amount) >= ((int(limit) * 90) / 100)) and (transactionAmount == 1)


#Check if the same merchant has more than 10 transactions (4)
def funcMoreThanTen(merchantName, totalTransactionsUser):
    aboveLimitTransaction = merchant.query.filter_by(name=merchantName)
    for transaction in aboveLimitTransaction:
        totalTransactions = transaction.transactionAmount
    return totalTransactionsUser > 10

#Check if transaction amount value was negative
def funcCheckIfNegative(amount):
    return int(amount) < 0

#Check if Account is whitelisted.
def funcCheckWhitelisted(isWhitelisted):
    return isWhitelisted == "False"



@app.route('/api/v1.0/validate/transaction', methods=['POST'])
def validator():


        global transactionAmount
        transactionAmount += 1
        lastAllTransactionsAmount = 0
        if request.method == 'POST':

            dataFromJson = request.data
            inputData = json.loads(dataFromJson)

            #Populate Variables with key Account values at JSON data
            for accountObjects in inputData['Account']:
                cardIsActive = accountObjects['cardIsActive']
                limit = accountObjects['limit']
                blacklist = accountObjects['blacklist']
                isWhitelisted = accountObjects['isWhitelisted']

            #Populate Variables with key Transaction values at JSON data
            for transactionObjects in inputData['Transaction']:
                merchantName = transactionObjects['merchant']
                amount = transactionObjects['amount']
                transactionTime = transactionObjects['time']

            #Populate Variables with key LastTransactions values at JSON data
            for lastTransactionsObject in inputData['LastTransactions']:
                lastTransactionsValues = lastTransactionsObject['Transactions']
            for i in range(0, len(lastTransactionsValues)):
                lastAllTransactionsAmount += lastTransactionsValues[i]

        nameInDB = []
        #If merchant name doesn't exist in DB, insert a new merchant.
        objectMerchant = merchant.query.all()
        for name in objectMerchant:
            nameInDB.append(name.name)

        if merchantName in nameInDB:
            updateTransactionAmount = merchant.query.filter_by(name=merchantName).first()
            updateTransactionAmount.transactionAmount += 1
            db.session.commit()
            totalTransactionsUser = updateTransactionAmount.transactionAmount
        else:
            newMerchant = merchant(None, merchantName, False, 1)
            db.session.add(newMerchant)
            db.session.commit()
            updateTransactionAmount = merchant.query.filter_by(name=merchantName).first()
            totalTransactionsUser = updateTransactionAmount.transactionAmount


############  Running Functions to check the results and return a HTTP response based on JSON Post ############

        if funcCheckWhitelisted(isWhitelisted):
            return jsonify({'Invalid Transaction': 'The card is not in whitelist'}), 400

        if funcCardIsActive(cardIsActive):
            return jsonify({'Invalid Transaction' : 'Card is Blocked'}),400

        if funcValidateTransaction(amount, limit, lastAllTransactionsAmount):
            return jsonify({'Invalid Transaction' : 'The transaction value is greater than the limit.'}), 400

        if funcCheckFirstTransaction(amount, limit, transactionAmount):
            return jsonify({'Invalid Transaction' : 'The first transaction can\'t be greater than 90% of the limit.'}), 400

        if funcMoreThanTen(merchantName, totalTransactionsUser):
            return jsonify({'Invalid Transaction': 'The same merchant has more than 10 transactions.'}), 400

        if funcCheckIfNegative(amount):
            return jsonify({'Invalid Transaction' : 'The transaction amount can\'t be negative'}), 400

        return jsonify({'Transaction Status:' : 'Authorized'},
                       {'Available Limit:' : (limit-lastAllTransactionsAmount) - amount})

############  // Running Functions to check the results and return a HTTP response based on JSON Post //  ############


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

