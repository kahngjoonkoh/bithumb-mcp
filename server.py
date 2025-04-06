import os
from typing import Optional, List
from decimal import Decimal
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP
from pybithumb2 import BithumbClient, MarketID, TradeSide, OrderType, OrderID

load_dotenv()
API_KEY = os.getenv("API_KEY_ID")
API_SECRET = os.getenv("API_SECRET_KEY")

if not API_KEY or not API_SECRET:
    raise ValueError("Bithumb API credentials not found in environment variables.")

# Initialize FastMCP server
mcp = FastMCP("Bithumb API", dependencies=["pybithumb2", "python-dotenv"])

client = BithumbClient(API_KEY, API_SECRET, use_raw_data=True)


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


# @mcp.tool()
# async def get_minute_candles(
#     market: str,
#     to: Optional[str] = None
#     count: int = 1
#     unit:
# )


if __name__ == "__main__":
    mcp.run()
