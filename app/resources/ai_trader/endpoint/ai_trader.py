from threading import Thread

from flask import jsonify

from app.services.ai_trader import CryptoTrader

from ..namespace.ai_trader import ai_trader_namespace

trader = CryptoTrader(
    api_key="your_api_key", api_secret="your_api_secret", openai_key="your_openai_key"
)
trader_thread = None


@ai_trader_namespace.route("/start", methods=["POST"])
def start_trading():
    global trader_thread
    if trader_thread is None or not trader_thread.is_alive():
        trader_thread = Thread(target=trader.main)
        trader_thread.start()
        return jsonify({"message": "Trading started"}), 200
    else:
        return jsonify({"message": "Trading is already running"}), 200


@ai_trader_namespace.route("/stop", methods=["POST"])
def stop_trading():
    if trader_thread is not None:
        trader.stop_trading = True
        trader_thread.join()
        return jsonify({"message": "Trading stopped"}), 200
    else:
        return jsonify({"message": "Trading is not running"}), 404


@ai_trader_namespace.route("/status", methods=["GET"])
def trading_status():
    if trader_thread is not None and trader_thread.is_alive():
        return jsonify({"status": "running"}), 200
    else:
        return jsonify({"status": "stopped"}), 200


@ai_trader_namespace.route("/trades", methods=["GET"])
def get_trades():
    trades = trader.get_trades()
    return jsonify(trades), 200
