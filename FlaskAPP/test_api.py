import unittest
from app import app
import json


class TestValidateFunctins(unittest.TestCase):

    def test_validate_transaction(self):
        newDict = {"Account": [
            {"cardIsActive": "True", "limit": 9200, "blacklist": ["BadPay", "Hooka"], "isWhitelisted": "True"}],
                   "Transaction": [{"merchant": "renato", "amount": 500, "time": "15-Dezembro-2012"}],
                   "LastTransactions": [{"Transactions": [200, 300, 600]}]}
        test_object = app.test_client(self)
        response = test_object.post('/api/v1.0/validate/transaction', data=json.dumps(newDict), content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_card_is_active(self):
        cardBlocked = {"Account": [
            {"cardIsActive": "False", "limit": 9200, "blacklist": ["BadPay", "Hooka"], "isWhitelisted": "True"}],
            "Transaction": [{"merchant": "renato", "amount": 500, "time": "15-Dezembro-2012"}],
            "LastTransactions": [{"Transactions": [200, 300, 600]}]}
        test_object = app.test_client(self)
        response = test_object.post('/api/v1.0/validate/transaction', data=json.dumps(cardBlocked), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_check_first_transaction(self):
        firstTransaction = {"Account": [
            {"cardIsActive": "False", "limit": 9200, "blacklist": ["BadPay", "Hooka"], "isWhitelisted": "True"}],
            "Transaction": [{"merchant": "renato", "amount": 9000, "time": "15-Dezembro-2012"}],
            "LastTransactions": [{"Transactions": [200, 300, 600]}]}
        test_object = app.test_client(self)
        response = test_object.post('/api/v1.0/validate/transaction', data=json.dumps(firstTransaction), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_func_check_negative(self):
        checkNegative = {"Account": [
            {"cardIsActive": "False", "limit": 9200, "blacklist": ["BadPay", "Hooka"], "isWhitelisted": "True"}],
            "Transaction": [{"merchant": "renato", "amount": -900, "time": "15-Dezembro-2012"}],
            "LastTransactions": [{"Transactions": [200, 300, 600]}]}
        test_object = app.test_client(self)
        response = test_object.post('/api/v1.0/validate/transaction', data=json.dumps(checkNegative), content_type='application/json')
        self.assertEqual(400, response.status_code)


    def test_greater_than_limit(self):
        transactionObject = {"Account": [
            {"cardIsActive": "True", "limit": 9200, "blacklist": ["BadPay", "Hooka"], "isWhitelisted": "True"}],
            "Transaction": [{"merchant": "renato", "amount": 9900, "time": "15-Dezembro-2012"}],
            "LastTransactions": [{"Transactions": [200, 300, 600]}]}
        test_object = app.test_client(self)
        response = test_object.post('/api/v1.0/validate/transaction', data=json.dumps(transactionObject), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_check_whitelisted(self):
        check_whitelisted = {"Account": [
            {"cardIsActive": "True", "limit": 9200, "blacklist": ["BadPay", "Hooka"], "isWhitelisted": "False"}],
            "Transaction": [{"merchant": "renato", "amount": 200, "time": "15-Dezembro-2012"}],
            "LastTransactions": [{"Transactions": [200, 300, 600]}]}
        test_object = app.test_client(self)
        response = test_object.post('/api/v1.0/validate/transaction', data=json.dumps(check_whitelisted), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_more_than_ten(self):
        data_post = {"Account": [
            {"cardIsActive": "True", "limit": 9200, "blacklist": ["BadPay", "Hooka"], "isWhitelisted": "False"}],
            "Transaction": [{"merchant": "TentOculos", "amount": 200, "time": "15-Dezembro-2012"}],
            "LastTransactions": [{"Transactions": [200, 300, 600]}]}
        test_object = app.test_client(self)
        for i in range(1,12):
            test_object.post('/api/v1.0/validate/transaction', data=json.dumps(data_post), content_type='application/json')
        response = test_object.post('/api/v1.0/validate/transaction', data=json.dumps(data_post), content_type='application/json')
        self.assertEqual(400, response.status_code)





if __name__ == '__main__':
    unittest.main()

