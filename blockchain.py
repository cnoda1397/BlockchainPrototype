# Blockchain Prototype Project By Collyn Noda

import datetime

# Calculate the hash to add digital fingerprint
import hashlib
from itertools import chain

# Store data in JSON
import json
from random import randrange
from secrets import randbelow

# flask for creating web app
# jsonify for displaying th blockain
from flask import Flask, jsonify

class Blockchain:
    # Create the first block and set hash to "0"
    def __init__(self):
        self.chain = []
        first_block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': 1,
            'previous_hash': '0',
            'payload': str(randbelow(10))
        }
        self.chain.append(first_block)
        #self.create_block(proof=1, previous_hash='0')
    
    # Add blocks to the chain
    def create_block(self, proof, previous_hash, payload=-1):
        if payload < 0:
            payload=randbelow(10)
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'payload': self.get_previous_block()['payload'] + (str(payload))
        }
        self.chain.append(block)
        return block
    
    # get the previous block
    def get_previous_block(self):
        return self.chain[-1]

    # create the proof of work that allows access to the block
    def get_proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
        
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_is_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                print('flag 1')
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] != '00000':
                print(hash_operation)
                return False

            previous_block = block
            block_index += 1
        
        return True
#################################################################################################################################
# create web app via flask
app = Flask(__name__)

# create instance of blockchain
blockchain = Blockchain()

# Mine a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof =  previous_block['proof']
    proof = blockchain.get_proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    response = {
        'message': 'A block has been MINED',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'payload': block['payload']
    }

    return jsonify(response), 200

@app.route('/custom_block/<int:num>', methods=['GET'])
def custom_block(num:int):
    previous_block = blockchain.get_previous_block()
    previous_proof =  previous_block['proof']
    proof = blockchain.get_proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash, num)

    response = {
        'message': 'A block has been MINED',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'payload': block['payload']
    }

    return jsonify(response), 200

# display blockchain in json format
@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200

# check the validity
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_is_valid(blockchain.chain)
    
    if valid:
        response = {'message': 'The Blockchain is Valid'}
    else:
        response = {'message': 'The Blockchain is NOT Valid'}

    return jsonify(response), 200

# Run locally
app.run(host='127.0.0.1', port=5000)