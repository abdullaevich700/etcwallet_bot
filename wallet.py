import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from web3 import Web3

Token = '6829200810:AAEfe_ov5O3IoXsWezlzP--yXtaN9l0GhZg'

bot = Bot(Token)
dp = Dispatcher(bot)
w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/c68838e622a1432388f9cd9f8d4da98e'))
contract_address = "0x591a4d3dD91668cA0441e492f10C646f17906A11"
print("Contract Address:", contract_address)
contract_abi = [
    {
        "inputs": [],
        "stateMutability": "payable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "Deposit",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "PasswordChanged",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "SentTo",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "WalletBlocked",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "WalletUnblocked",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "Withdrawal",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "blockWallet",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "newPassword",
                "type": "string"
            }
        ],
        "name": "changePassword",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "destroy",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getBalance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "isWalletBlocked",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address payable",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {

                "internalType": "address payable",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "sendTo",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "password",
                "type": "string"
            }
        ],
        "name": "unblockWallet",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "userWallets",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "password",
                "type": "string"
            }
        ],
        "name": "verifyPassword",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "withdraw_amount",
                "type": "uint256"
            }
        ],
        "name": "withdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "stateMutability": "payable",
        "type": "receive"
    }
]

faucet_contract = w3.eth.contract(address=contract_address, abi=contract_abi)


def get_user_address(chat_id):
    user_address = w3.eth.account.create().address
    return user_address


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_address = get_user_address(message.chat.id)
    await message.reply(f"Welcome! Your Ethereum address is: {user_address}")

@dp.message_handler(commands=['balance'])
async def balance(message: types.Message):
    user_address = get_user_address(message.chat.id)
    balance = None

    try:
        gas_limit = 5000000  
        gas_price = 2000000000
        balance = faucet_contract.functions.getBalance().call({'from': user_address, 'gas': gas_limit, 'gas_price': gas_price})
        print(f"Balance: {balance} wei")
    except Exception as e:
        print(f"Error getting balance: {type(e).__name__} - {str(e)}")
        print(f"Infura URL: {w3.provider.endpoint_uri}")
        print(f"Network ID: {w3.net.version}")
        print(f"Gas Price: {gas_price}")

    if balance is not None:
        await message.reply(f"Your balance is: {balance} wei")
    else:
        await message.reply("There was an error retrieving your balance.")



@dp.message_handler(commands=['send'])
async def send_to(message: types.Message):
    user_address = get_user_address(message.chat.id)

    try:
        _, to_address, amount_str = message.text.split(' ')
        amount = int(amount_str)
    except ValueError:
        await message.reply("Invalid format. Please use: /send <to_address> <amount>")
        return

    try:
        transaction_hash = faucet_contract.functions.sendTo(to_address, amount).transact({'from': user_address})
        await message.reply(f"Sent {amount} wei to {to_address}. Transaction hash: {transaction_hash.hex()}")
    except Exception as e:
        await message.reply(f"Failed to send Ether. Error: {str(e)}")


@dp.message_handler(commands=['withdraw'])
async def withdraw(message: types.Message):
    user_address = get_user_address(message.chat.id)
    withdraw_amount = 100000000000000000  
    try:
        transaction_hash = faucet_contract.functions.withdraw(withdraw_amount).transact({'from': user_address})
        await message.reply(f"Withdrawal successful. Transaction hash: {transaction_hash.hex()}")
    except Exception as e:
        await message.reply(f"Withdrawal failed. Error: {str(e)}")


@dp.message_handler(commands=['block'])
async def block_wallet(message: types.Message):
    user_address = get_user_address(message.chat.id)
    try:
        faucet_contract.functions.blockWallet().transact({'from': user_address})
        await message.reply("Wallet blocked successfully.")
    except Exception as e:
        await message.reply(f"Failed to block wallet. Error: {str(e)}")


@dp.message_handler(commands=['unblock'])
async def unblock_wallet(message: types.Message):
    user_address = get_user_address(message.chat.id)
    password = "defaultPassword"  
    try:
        faucet_contract.functions.unblockWallet(password).transact({'from': user_address})
        await message.reply("Wallet unblocked successfully.")
    except Exception as e:
        await message.reply(f"Failed to unblock wallet. Error: {str(e)}")


@dp.message_handler(commands=['changepassword'])
async def change_password(message: types.Message):
    user_address = get_user_address(message.chat.id)
    new_password = "newPassword"  
    try:
        faucet_contract.functions.changePassword(new_password).transact({'from': user_address})
        await message.reply("Password changed successfully.")
    except Exception as e:
        await message.reply(f"Failed to change password. Error: {str(e)}")


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
