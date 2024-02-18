import csv

data = {
    'type': 'TRANSFER',
    'amount': '',
    'nameOrig': '',
    'oldBalanceOrg': '',
    'newBalanceOrig': '',
    'nameDest': '',
    'oldbalanceDest': '',
    'newBalanceDest': '',
    'transactionID':  ''
}

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['step', 'type', 'amount', 'nameOrig', 'oldBalanceOrg', 'newBalanceOrig', 'nameDest', 'oldbalanceDest', 'newBalanceDest', 'transactionID']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'step': '1',
                     'type': data['type'],
                     'amount': data['amount'],
                     'nameOrig': data['nameOrig'],
                     'oldBalanceOrg': data['oldBalanceOrg'],
                     'newBalanceOrig': data['amount'],
                     'nameDest': data['amount'],
                     'oldbalanceDest': data['oldbalanceDest'],
                     'newBalanceDest': data['newBalanceDest'],
                     'transactionID': data['transactionID']
                     })
