from web3 import Web3
from flask_cors import CORS
from flask import Flask, request
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from Crypto.Cipher import AES
import base64
from Crypto.Protocol.KDF import PBKDF2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("firebase-admin.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://gezivr-7dc1c-default-rtdb.europe-west1.firebasedatabase.app'
    })
ref = db.reference('/')

app = Flask(__name__)
CORS(app)

web3 = Web3(Web3.HTTPProvider('https://sepolia.gateway.tenderly.co/5r6g2NgpfRUP7grlfliq5I'))
receiver = "0xBf91DAb45845dAB73C1566b0eFA30e79A4DBEe69"

@app.route('/')
def index():
    return "Hello World!"

def toEther(amount):
    float_val = float(amount)
    return float_val / (10 ** 18)

@app.route('/getBalance/<address>')
def getBalance(address):
    balance = web3.eth.get_balance(address, 'latest')
    balance = toEther(balance)
    return str(balance)

#gezivr privatekey 1c133ce01ec9718fbb2fd514527956694540e1c52110eacd3ea7d9a269b4606e
def toWei(amount):
    float_val = float(amount)
    return int(float_val * (10 ** 18))

@app.route('/getPrivateKey', methods=['GET','POST'])
def getPrivateKey():
    title = request.get_json()["title"]
    encrypt = request.get_json()["content"]
    length = request.get_json()["length"]
    key = decrypt(encrypt, length)
    
    return key
   
def decrypt(encrypted_key, length):
    key_bytes = bytes("1c133ce01ec9718fbb2fd514527956694540e1c52110eacd3ea7d9a269b4606e", 'utf-8')
    salt = b'\x01\x23\x45\x67\x89\xAB\xCD\xEF'
    derived_key = PBKDF2(key_bytes, salt, dkLen=32, count=10000)

    iv = b'\x00' * 16
    cipher = AES.new(derived_key, AES.MODE_CBC, iv)
    encrypted_bytes = base64.b64decode(encrypted_key)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)
    decrypted_bytes = decrypted_bytes.decode('utf-8').rstrip('\0')
    return decrypted_bytes[:length]

def sendTransaction(address, amount, private_key):
    sender = {
        "private_key": private_key, 
        "address": address,
    }
    try:
        web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
        tx_create = web3.eth.account.sign_transaction(
        {
            "nonce": web3.eth.get_transaction_count(sender["address"]),
            "gasPrice": web3.eth.generate_gas_price(),
            "gas": 21000,
            "to": receiver,
            "value":toWei(amount),
            "chainId": 11155111
        },
        sender["private_key"]
        )
        tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
        print(tx_hash)
        return "Success"
        #tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    except:
        return "Failed"
    
@app.route("/sendTransaction", methods=['POST'])
def sendTransaction2():
    userId = request.get_json()["userId"]
    amount = request.get_json()["amount"]
    print(userId)
    print(amount)
    privateKey = ref.child("users").child(str(userId)).child("privateKey").get()
    decryptedKey = decrypt(privateKey["privateKey"], privateKey["length"])
    accountAddress = ref.child("users").child(str(userId)).child("accountAddress").get()
    return sendTransaction(accountAddress, amount, decryptedKey)

@app.route("/setPaymentInfo", methods=['POST'])
def setPaymentInfo():
    userId = request.get_json()["userId"]
    accountAddress = request.get_json()["accountAddress"]
    en_privateKey = request.get_json()["en_privateKey"]
    length = request.get_json()["length"]

    ref.child("users").child(str(userId)).child("accountAddress").set(accountAddress)
    json = {
        "length": length,
        "en_privateKey": en_privateKey
    }
    ref.child("users").child(str(userId)).child("private_key").set(json)
    return "Done"


#if __name__ == '__main__':
#    app.run()