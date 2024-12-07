import logging
import signal
import time
from datetime import datetime

import openai
# from coinbase.rest import RESTClient

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class CryptoTrader:
    def __init__(self, api_key, api_secret, openai_key):
        # self.client = RESTClient(api_key=api_key, api_secret=api_secret, timeout=10000)
        openai.api_key = openai_key
        self.logger = logging.getLogger(self.__class__.__name__)
        self.stop_trading = False
        self.trades = []

    def handle_stop_signal(self, signum, frame):
        self.logger.info("Received stop signal. Halting trading.")
        self.stop_trading = True

    def check_stop_condition(self):
        return self.stop_trading

    def make_llm_trade_decision(self, prompt):
        try:
            enhanced_prompt = (
                f"{prompt}\n"
                "You are an expert day trader utilizing a KNN prediction model for market analysis. "
                "Recent price movements indicate either an upward or downward trend. "
                "If the trend is positive and strong, respond with BUY. "
                "If the trend is negative and strong, respond with SELL. "
                "If the trend is unclear or weak, respond with HOLD. "
                "Based on this prediction and your strategy, should we BUY, SELL, or HOLD? Respond with one word: BUY, SELL, or HOLD."
            )
            self.logger.debug(f"Sending enhanced prompt to LLM:\n{enhanced_prompt}")

            response = openai.Completion.create(
                model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
                prompt=enhanced_prompt,
                max_tokens=100,
                temperature=0.0,
            )

            reply = response["choices"][0]["text"].strip().upper()
            if reply in ["BUY", "SELL", "HOLD"]:
                return reply
            else:
                self.logger.warning("Invalid response from LLM, defaulting to HOLD.")
                return "HOLD"
        except Exception as e:
            self.logger.exception("Failed to communicate with LLM.")
            return "HOLD"

    def get_product_book(self, product_id):
        try:
            product_book_data = self.client.get_product_book(
                product_id=product_id, limit=100
            )
            pricebook = product_book_data.get("pricebook", {})
            bids = pricebook.get("bids", [])
            asks = pricebook.get("asks", [])

            best_bid = float(bids[0]["price"]) if bids else None
            best_ask = float(asks[0]["price"]) if asks else None

            if best_bid is None or best_ask is None:
                return None, None, None

            return f"Best Bid: {best_bid}, Best Ask: {best_ask}", best_bid, best_ask
        except Exception as e:
            self.logger.exception(f"Error fetching product book: {e}")
            return None, None, None

    def get_balances(self):
        try:
            response = self.client.get_accounts()
            accounts = response.get("accounts", [])
            btc_balance = next(
                (
                    float(account["available_balance"]["value"])
                    for account in accounts
                    if account["currency"] == "BTC"
                ),
                0,
            )
            usdc_balance = next(
                (
                    float(account["available_balance"]["value"])
                    for account in accounts
                    if account["currency"] == "USDC"
                ),
                0,
            )
            return btc_balance, usdc_balance
        except Exception as e:
            self.logger.exception("Failed to retrieve account balances.")
            return 0, 0

    def market_order_buy(self, price):
        amount_usdc = 2.00
        btc_bought = amount_usdc / price
        self.trades.append(
            {
                "type": "buy",
                "amount": btc_bought,
                "price": price,
                "timestamp": datetime.now(),
            }
        )
        self.logger.info(f"Buy order placed at {price:.2f} USDC/BTC.")

    def market_order_sell(self, price):
        amount_usdc = 2.00
        btc_sold = amount_usdc / price
        self.trades.append(
            {
                "type": "sell",
                "amount": btc_sold,
                "price": price,
                "timestamp": datetime.now(),
            }
        )
        self.calculate_profit_loss()
        self.logger.info(f"Sell order placed at {price:.2f} USDC/BTC.")

    def calculate_profit_loss(self):
        if len(self.trades) >= 2:
            buys = [trade for trade in self.trades if trade["type"] == "buy"]
            sells = [trade for trade in self.trades if trade["type"] == "sell"]
            if buys and sells:
                last_buy = buys[-1]
                last_sell = sells[-1]
                profit_loss = (last_sell["amount"] * last_sell["price"]) - (
                    last_buy["amount"] * last_buy["price"]
                )
                last_sell["profit_loss"] = profit_loss
                self.logger.info(f"Profit/Loss for last trade: {profit_loss:.2f} USDC.")

    def get_trades(self):
        return self.trades

    def main(self):
        signal.signal(signal.SIGINT, self.handle_stop_signal)
        signal.signal(signal.SIGTERM, self.handle_stop_signal)
        self.logger.info("Starting trading loop...")
        while not self.check_stop_condition():
            btc_balance, usdc_balance = self.get_balances()
            if btc_balance is None or usdc_balance is None:
                self.logger.warning("Failed to retrieve balances.")
                time.sleep(2)
                continue

            prompt, best_bid, best_ask = self.get_product_book("BTC-USDC")
            if not prompt or not best_bid or not best_ask:
                time.sleep(2)
                continue

            decision = self.make_llm_trade_decision(prompt)
            if decision == "BUY" and usdc_balance > 0:
                self.market_order_buy(best_bid)
            elif decision == "SELL" and btc_balance > 0:
                self.market_order_sell(best_ask)
            else:
                self.logger.info("HOLD decision or insufficient balance.")
            time.sleep(2)
