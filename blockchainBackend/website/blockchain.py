from flask import Blueprint, request, jsonify
from AESCipher import AESCipher
from sklearn.preprocessing import StandardScaler
from datetime import datetime

import pandas as pd

import joblib

from web3 import Web3

import binascii

from flask_cors import cross_origin

blockchain = Blueprint('blockchain', __name__)


infura_http_url = 'https://goerli.infura.io/v3/5c3c3009ee5d452ba5b150e7f38edb5a'
web3 = Web3(Web3.HTTPProvider(infura_http_url))

abi = [
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "adminUid",
                "type": "bytes32"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "string",
                "name": "sender",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "bytes[]",
                "name": "data",
                "type": "bytes[]"
            }
        ],
        "name": "DataStored",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "transactionId",
                "type": "string"
            },
            {
                "internalType": "bytes",
                "name": "_data",
                "type": "bytes"
            }
        ],
        "name": "storeData",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "transactionId",
                "type": "string"
            },
            {
                "internalType": "bytes32",
                "name": "adminUid",
                "type": "bytes32"
            }
        ],
        "name": "returnData",
        "outputs": [
                {
                    "internalType": "bytes[]",
                    "name": "data",
                    "type": "bytes[]"
                }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

address = "0x11C477EA902F75EDB6Ec11C0831159Ea0c96aB9f"

contract = web3.eth.contract(address=address, abi=abi)

private_key = 'c624252bf44391a8e2212bc99b3a593e968ccaeeb5f7437fe40cd57a08ae94a1'


def change_val(file):
    datapd = pd.read_csv(file).iloc[-1]

    datapd.drop(['transactionID'], axis=1)
    col = ['amount', 'oldbalanceOrg', 'newbalanceOrig',
           'oldbalanceDest', 'newbalanceDest']
    features = datapd[col]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    scaled_features = pd.DataFrame(scaled_features, columns=col)

    data_encode = datapd['type']
    dummy = pd.get_dummies(data_encode, drop_first=True)
    data_fraud = datapd['isFraud']

    dt = datapd.copy()
    cols = ['nameOrig', 'nameDest']
    dt[cols] = dt[cols].astype('category')
    for i in cols:
        dt[i] = dt[i].cat.codes
    know = dt[['nameOrig', 'nameDest']]

    flagged = datapd['isFlaggedFraud']

    new_datapd = pd.concat([dummy, know, scaled_features, flagged], axis=1)

    col1 = ['nameOrig', 'nameDest']
    features1 = new_datapd.drop(col1, axis=1)  # Exclude categorical columns
    scaler1 = StandardScaler()
    features1 = scaler1.fit_transform(features1)
    know1 = pd.DataFrame(features1, columns=col1)

    new_datapd['nameOrig'] = know1['nameOrig']
    new_datapd['nameDest'] = know1['nameDest']

    return new_datapd


@blockchain.route('/store', methods=['POST'])
@cross_origin(origin='*')
def store():
    timestamp = int(round(datetime.now().timestamp()))
    model = joblib.load("aml_final.pkl")

    data = request.get_json()

    data_encryption = AESCipher("admin@123")

    #  Check if txn is fraud or not
    transaction_data = {'step': '1',
                        'type': data['type'],
                        'amount': data['amount'],
                        'nameOrig': data['nameOrig'],
                        'oldBalanceOrg': data['oldBalanceOrg'],
                        'newBalanceOrig': data['amount'],
                        'nameDest': data['amount'],
                        'oldbalanceDest': data['oldbalanceDest'],
                        'newBalanceDest': data['newBalanceDest'],
                        'transactionID': data['id']
                        }

    # enc = data_encryption.encrypt_bytes32(transaction_data)

    csv_subset = f"test.csv"

    fieldnames = ['step', 'type', 'amount', 'nameOrig', 'oldBalanceOrg',
                  'newBalanceOrig', 'nameDest', 'oldbalanceDest', 'newBalanceDest', 'transactionID']

    #     if not os.path.exists(csv_subset):
    #          with open(csv_subset,'w') as file:
    #           writer = csv.DictWriter(file, fieldnames=fieldnames)
    #           writer.writeheader()
    #           file.close()

    # with open(csv_subset, 'w', newline='') as csvfile:
    #      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    #      writer.writeheader()
    #      writer.writerow({'step': '1',
    #                          'type': data['type'],
    #                          'amount': data['amount'],
    #                          'nameOrig': data['nameOrig'],
    #                          'oldBalanceOrg': data['oldBalanceOrg'],
    #                          'newBalanceOrig': data['amount'],
    #                          'nameDest': data['amount'],
    #                          'oldbalanceDest': data['oldbalanceDest'],
    #                          'newBalanceDest': data['newBalanceDest'],
    #                          'transactionID': data['id']
    #                          })

    # Upload data to blockchain

    # Input data txnId and data as bytes
    enc_data = data_encryption.encrypt_bytes32('suspicious')

    transaction_id = transaction_data['transactionID']

    function_call = contract.functions.storeData(transaction_id, enc_data).build_transaction(
        {"nonce": web3.eth.get_transaction_count('0x53B1d6eed8e25f0d131D4987909Fa91A50f04CDa')})

    signed_transaction = web3.eth.account.sign_transaction(
        function_call, private_key)

    # Send the signed transaction to the Ethereum network
    transaction_hash = web3.eth.send_raw_transaction(
        signed_transaction.rawTransaction)

    # Wait for the transaction to be mined (optional)
    web3.eth.wait_for_transaction_receipt(transaction_hash)

    return jsonify({'message': 'success'})


@blockchain.route('/view', methods=['POST'])
@cross_origin(origin='*')
def retrieve():
    data = request.get_json()

    key = '0x0ee273a7affa4c0f6caa2c6be14fa0466ae6e314771e6561022a4b0de8bc1c69'

    transaction_id = data['transaction_id']

    block_data = contract.functions.returnData(transaction_id, key).call()

    data_encryption = AESCipher("admin@123")

    converted = b'0x'+binascii.hexlify(block_data[0])

    converted = converted.decode('utf-8')

    retrieved_data = data_encryption.decrypt_bytes32(converted)

    return jsonify({'txn_id':transaction_id,'status': retrieved_data})
