from web3 import Web3
from flask import Flask

app = Flask(__name__)

alchemy_url = "https://eth-sepolia.g.alchemy.com/v2/UVNWjjrTK8MIr6-CD92dUIYj1NI6RjPb"
w3 = Web3(Web3.HTTPProvider(alchemy_url))
# Print if web3 is successfully connected
print(w3.is_connected())
balance = w3.eth.get_balance('0xBf91DAb45845dAB73C1566b0eFA30e79A4DBEe69')
print(balance)

latest_block = w3.eth.block_number
print(latest_block)

@app.route('/')
def index():
    alchemy_url = "https://eth-sepolia.g.alchemy.com/v2/UVNWjjrTK8MIr6-CD92dUIYj1NI6RjPb"
    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    # Print if web3 is successfully connected
    
    balance = w3.eth.get_balance('0xBf91DAb45845dAB73C1566b0eFA30e79A4DBEe69')
    
    return w3.is_connected(), balance

    

  
#if __name__ == '__main__':
#    app.run()