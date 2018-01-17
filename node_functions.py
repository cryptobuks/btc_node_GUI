import json, datetime
import bitcoin
from bitcoin.rpc import *

PROXY = Proxy()

def convert_unixtime(unixtime):
	time_stamp = datetime.datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
	return time_stamp

def get_block_info(block):
	block_hash = PROXY.call('getblockhash', block)
	block_info = PROXY.call('getblock', block_hash)
	return json.dumps(block_info, indent=4)

def get_best_block_info():
	best_block_hash = PROXY.call('getbestblockhash')
	block_info = PROXY.call('getblock', best_block_hash)

	block_dict = {
		'height': int(block_info['height']),
		'confirmations': int(block_info['confirmations']),
		'time': convert_unixtime(block_info['time']),
		'mediantime': convert_unixtime(block_info['mediantime']),
		'weight': int(block_info['weight']),
		'size': int(block_info['size']),
		'strippedsize': int(block_info['strippedsize'])
	}
	return block_dict

def get_connections_info():
	connection_count = PROXY.call('getconnectioncount')
	peers = PROXY.call('getpeerinfo')

	final_dict = dict()

	peers_list = []
	for peer in peers:
		peer_dict = {
			'id': peer['id'],
			'version': peer['subver'],
			'ip_address': peer['addr'],
			'last_received': convert_unixtime(peer['lastrecv']),
		}
		if peer['synced_blocks'] is not -1:
			peer_dict['synced_blocks'] = peer['synced_blocks']
		else:
			peer_dict['synced_blocks'] = 'light client'
		peers_list.append(peer_dict)

	final_dict['peers'] = peers_list
	return final_dict

def create_new_address(account):
	recv_address = PROXY.call('getnewaddress', account)
	return recv_address

def get_balance(account):
	acct_balance = PROXY.call('getbalance', account)
	return acct_balance

def get_wallet_info():
	wallet_info = PROXY.call('getwalletinfo')

	wallet_dict = {
		'unconfirmed_balance': float(wallet_info['unconfirmed_balance']),
		'balance': float(wallet_info['balance']),
		'tx_count': wallet_info['txcount']
	}
	return wallet_dict

def get_transactions():
	transactions = PROXY.call('listtransactions')

	transactions_list = []
	for tx in transactions:
		transactions_dict = {
			'account': tx['account'],
			'category': tx['category'],
			'amount': float(tx['amount']),
			'time_received': convert_unixtime(tx['timereceived'])
		}
		transactions_list.append(transactions_dict)
	return transactions_list

if __name__ == '__main__':
	#print(get_wallet_info())
	print(create_new_address('dan'))