import json
import flask as fl
from flask import Flask, Response, request
import node_functions as func

app = Flask(__name__)

@app.route('/node/block', methods=['GET'])
def serve_block_info():
	block_dict = func.get_best_block_info()
	return fl.render_template('block.html', block_dict=block_dict)

@app.route('/node/connections', methods=['GET'])
def serve_connections_info():
	connections = func.get_connections_info()
	connections_list = connections['peers']
	return fl.render_template('connections.html', connections_list=connections_list)

@app.route('/node/wallet', methods=['GET'])
def serve_wallet_info():
	wallet_dict = func.get_wallet_info()
	transactions_list = func.get_transactions()
	return fl.render_template('wallet.html', wallet_dict=wallet_dict, transactions_list=transactions_list)

@app.route('/node', methods=['GET'])
def serve_dash():
	return fl.render_template('dash.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=44444)