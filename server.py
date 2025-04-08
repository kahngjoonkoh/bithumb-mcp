import os
from typing import Optional, List
from decimal import Decimal
from tabulate import tabulate
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP
from pybithumb2 import BithumbClient, MarketID, TradeSide, OrderType, OrderID, TimeUnit

load_dotenv()
API_KEY = os.getenv("API_KEY_ID")
API_SECRET = os.getenv("API_SECRET_KEY")

if not API_KEY or not API_SECRET:
    raise ValueError("Bithumb API credentials not found in environment variables.")

# Initialize FastMCP server
mcp = FastMCP("Bithumb API", dependencies=["pybithumb2", "python-dotenv", "tabulate"])

client = BithumbClient(API_KEY, API_SECRET, use_raw_data=True)


def _format_helper(data: dict) -> str:
    return tabulate(data, headers="keys", tablefmt="plain")


@mcp.tool()
async def get_accounts() -> dict:
    """
    Fetches and returns the user's account balances for each asset.
    """
    return client.get_accounts()


@mcp.tool()
async def get_snapshots(markets: List[str]) -> dict:
    return client.get_snapshots(
        markets=[MarketID.from_string(market) for market in markets]
    )


@mcp.tool()
async def submit_order(
    market: str, side: str, volume: float, price: float, ord_type: str
) -> dict:
    """
    Submits an order.trade_side is either BID or ASK. ord_type is either Limit, Price, or Market. Price is the same as Limit but for selling.
    """
    return client.submit_order(
        MarketID.from_string(market),
        TradeSide(side),
        Decimal(volume),
        Decimal(price),
        OrderType(ord_type),
    )


@mcp.tool()
async def get_orders(market: Optional[str] = None) -> dict:
    """
    Fetches open orders. Can filter for a specific market.
    Args:
        market (str, optional): can filter by market. market will be parsed to Market. (e.g. KRW-BTC)

    Returns:
        dict: response
    """
    return client.get_orders(market=MarketID.from_string(market))


@mcp.tool()
async def cancel_order(uuid: str) -> dict:
    """
    Cancels an order when given an order ID.
    """
    return client.cancel_order(OrderID(uuid))


@mcp.tool()
async def get_markets() -> dict:
    """
    Returns a summary of available markets on Bithumb.
    """
    max_items = 30
    return client.get_markets(isDetails=True)[:max_items] + [
        {"note": f"...truncated to {max_items} results"}
    ]


@mcp.tool()
async def get_minute_candles(
    market: str, to: Optional[str] = None, count: int = 1, unit: int = 1
) -> str:
    """
    Fetches minute candlesticks for a given market.

    Args:
        market (str): The market to fetch minute candles for (e.g., "KRW-BTC").
        to (str, optional): A datetime with the format of (%Y-%m-%d %H:%M:%S) to limit the candlesticks to. Defaults to None.
        count (int, optional): The number of candles to fetch. Defaults to 1.
        unit (int, optional): The candle unit in minutes. Can only take values of 1, 3, 5, 10, 15, 30, 60, 240. Defaults to 1 minute.

    Returns:
        str: The response containing the minute candles data as a formatted table.
    """
    data = client.get_minute_candles(
        market=MarketID.from_string(str), to=to, count=count, unit=TimeUnit(unit)
    )
    # using tabulate instead of pandas as its more lightweight.
    return _format_helper(data)


@mcp.tool()
async def get_day_candles(
    market: str,
    to: Optional[str] = None,
    count: int = 1,
    unit: Optional[int] = 1,
    convertingPriceUnit: str = None,
) -> str:
    """
    Fetches minute candlesticks for a given market.

    Args:
        market (str): The market to fetch minute candles for (e.g., "KRW-BTC").
        to (str, optional): A datetime with the format of (%Y-%m-%d %H:%M:%S) to limit the candlesticks to. Defaults to None.
        count (int, optional): The number of candles to fetch. Defaults to 1.
        convertingPriceUnit (str, optional): The converting price unit as a symbol. (e.g. KRW, BTC)

    Returns:
        str: The response containing the day candles data as a formatted table.
    """
    data = client.get_day_candles(
        market=MarketID.from_string(str),
        to=to,
        count=count,
        convertingPriceUnit=convertingPriceUnit,
    )
    return _format_helper(data)


@mcp.tool()
async def get_week_candles(
    market: str,
    to: Optional[str] = None,
    count: int = 1,
) -> str:
    """
    Fetches minute candlesticks for a given market.

    Args:
        market (str): The market to fetch week candles for (e.g., "KRW-BTC").
        to (str, optional): A datetime with the format of (%Y-%m-%d %H:%M:%S) to limit the candlesticks to. Defaults to None.
        count (int, optional): The number of candles to fetch. Defaults to 1.

    Returns:
        str: The response containing the week candles data as a formatted table.
    """
    data = client.get_week_candles(market=MarketID.from_string(str), to=to, count=count)
    return _format_helper(data)


@mcp.tool()
async def get_month_candles(
    market: str,
    to: Optional[str] = None,
    count: int = 1,
) -> str:
    """
    Fetches minute candlesticks for a given market.

    Args:
        market (str): The market to fetch month candles for (e.g., "KRW-BTC").
        to (str, optional): A datetime with the format of (%Y-%m-%d %H:%M:%S) to limit the candlesticks to. Defaults to None.
        count (int, optional): The number of candles to fetch. Defaults to 1.

    Returns:
        str: The response containing the month candles data as a formatted table.
    """
    data = client.get_month_candles(
        market=MarketID.from_string(str), to=to, count=count
    )
    return _format_helper(data)


@mcp.tool()
async def get_trades(
    market: str, to: Optional[str] = None, count: int = 1, daysAgo: Optional[int] = None
) -> str:
    """
    Gets trade prices.

    Args:
        market (str): The market to fetch trade date for (e.g., "KRW-BTC").
        to (str, optional): A datetime with the format of (%Y-%m-%d %H:%M:%S) to limit the candlesticks to. Defaults to None in  which case fetches the most recent.
        count (int, optional): The number of trades to fetch. Defaults to 1.
        daysAgo (int, optional): Can get upto 7 days of data from the most recent trade. Takes in a number between 1 to 7.

    Returns:
        str: The response containing the trade data as a formatted table.
    """
    data = client.get_trades(
        market=MarketID.from_string(str), to=to, count=count, daysAgo=daysAgo
    )
    return _format_helper(data)


@mcp.tool()
async def get_orderbooks(markets: List[str]) -> str:
    """
    Gets trade prices.

    Args:
        markets (List[str]): A list of markets to fetch month candles for. Each market str is formated like "KRW-BTC".
    Returns:
        str: The response containing the orderbook data as a formatted table.
    """
    data = client.get_orderbooks(market=MarketID.from_string(str))
    return _format_helper(data)


@mcp.tool()
async def get_warning_markets() -> dict:
    """
    Gets virtual assets that are marked with warnings.
    """
    return client.get_warning_markets()


@mcp.tool()
async def get_wallet_status() -> dict:
    """
    Retrieves wallet and block statuses.
    """
    return client.get_wallet_status()


@mcp.tool()
async def get_api_keys() -> dict:
    """
    You can get your Bithumb API keys and the expiry dates.
    """
    return client.get_api_keys()


if __name__ == "__main__":
    mcp.run()
