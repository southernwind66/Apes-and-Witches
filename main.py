from web3 import Web3
from config import *
from infura import infura_url
import json
import pandas as pd

web3 = Web3(Web3.HTTPProvider(infura_url))

def getAllWitchOwners():
    w_address = Web3.toChecksumAddress(witch_address)
    witch_contract = web3.eth.contract(address=w_address, abi=witch_abi)
    witchSupply = witch_contract.functions.getLastTokenId().call()

    owners = []
    df = pd.DataFrame(columns=['Id', 'Address'])
    for i in range(1, witchSupply + 1):
        owner = witch_contract.functions.ownerOf(i).call()
        owners.append(owner)
        df.append({'Id': str(i), 'Address':owner}, ignore_index=True)
        if i % 100 == 0:
            print("Number of witches processed: " + str(i))
    df.to_csv("witchowners.csv", index=False)
    return owners

def getAllApeOwners():
    a_address = Web3.toChecksumAddress(ape_address)
    ape_contract = web3.eth.contract(address=a_address, abi=ape_abi)
    apeSupply = ape_contract.functions.totalSupply().call()

    owners = []
    df = pd.DataFrame(columns=['Id', 'Address'])
    for i in range(0, apeSupply):
        owner = ape_contract.functions.ownerOf(i).call()
        owners.append(owner)
        df.append({'Id': str(i), 'Address':owner}, ignore_index=True)
        if i % 100 == 0:
            print("Number of apes processed: " + str(i))
    df.to_csv("apeowners.csv", index=False)
    return owners

def getOwnersOfBoth(list1, list2):
    list1_as_set = set(list1)
    intersection = list1_as_set.intersection(list2)
    intersection_as_list = list(intersection)
    return intersection_as_list

witch_owners = getAllWitchOwners()
ape_owners = getAllApeOwners()
owners_of_both = getOwnersOfBoth(witch_owners, ape_owners)
print(owners_of_both)
print(len(owners_of_both))
