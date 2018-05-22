from argparse import ArgumentParser

import flask
from flask import Flask, request

from blockchain import Blockchain

app = Flask(__name__)
address = ''
blockchain = Blockchain()


@app.route('/')
def base():
    return flask.jsonify({
        'message': f'running on {address}',
        'chain': blockchain.blocs
    })


@app.route('/register/authority', methods=['POST'])
def set_auth():
    payload = request.get_json(force=True)

    if not payload['peer']:
        return flask.jsonify({
            'message': 'authority\'s address missing'
        }), 400

    blockchain.set_authority(payload['peer'])

    return flask.jsonify({
        'message': f"authority set at {payload['peer']}"
    })


@app.route('/register/node', methods=['POST'])
def new_node():
    payload = request.get_json(force=True)

    if not payload['peer']:
        return flask.jsonify({
            'message': 'peer\'s address missing'
        }), 400

    blockchain.register(payload['peer'])

    return flask.jsonify({
        'message': f"peer at {payload['peer']} added "
                   f"(total: {len(blockchain.peers)})"
    })


@app.route('/sync')
def sync():
    changed = blockchain.sync()
    return flask.jsonify({
        'message': 'chain updated' if changed else 'chain up to date'
    })


@app.route('/transaction/create', methods=['POST'])
def new_transaction():
    payload = request.get_json(force=True)

    blockchain.new_transaction(
        sender=address,
        content=payload
    )

    return flask.jsonify({
        'message': 'transaction added',
        'content': payload
    })


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-p',
        '--port',
        default=5000,
        type=int,
        help='port to listen on'
    )
    parser.add_argument(
        '-ht',
        '--host',
        default='127.0.0.1',
        type=str,
        help='peer\'s host'
    )
    args = parser.parse_args()

    port = args.port
    host = args.host

    address = f'{host}:{port}'

    app.run(host=host, port=port)
