from web3 import Web3
from flask import Flask
from web3.gas_strategies.rpc import rpc_gas_price_strategy


app = Flask(__name__)

web3 = Web3(Web3.HTTPProvider('https://sepolia.gateway.tenderly.co/5r6g2NgpfRUP7grlfliq5I'))
receiver = "0xBf91DAb45845dAB73C1566b0eFA30e79A4DBEe69"

@app.route('/')
def index():
    
    balance = web3.eth.get_balance(receiver, 'latest')
    print("Destination balance before transfer: ", balance)

    sender = {
        "private_key": "f74ee7c11f13b5d6d483cd48ea96914049a1852af1d394e2f104d761afa6a837", 
        "address": "0x6591C991210917184ec076A6D18D0f82B5e223bc",
    }
    
    web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
    tx_create = web3.eth.account.sign_transaction(
        {
            "nonce": web3.eth.get_transaction_count(sender["address"]),
            "gasPrice": web3.eth.generate_gas_price(),
            "gas": 21000,
            "to": receiver,
            "value": 310000000000000000,
            "chainId": 11155111
        },
        sender["private_key"]
        
    )
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    balance = web3.eth.get_balance(receiver, 'latest')
    print(balance)
    return f'Destination balance after transfer: {balance} ETH'

@app.route('/getBalance/<address>')
def getBalance(address):
    balance = web3.eth.get_balance(address, 'latest')
    return str(balance)

#if __name__ == '__main__':
#    app.run()