import json
from pathlib import Path
import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openbb import obb
import os
import asyncio
import time



# Global variable to track login status
is_logged_in = False

# Login to OpenBB with your PAT
async def login():
    global is_logged_in
    if is_logged_in:
        print("Already logged in. Skipping login.")
        return

    pat = os.getenv("OPENBB_PAT")  # Get the PAT from environment variable
    try:
        print("Attempting to log in with PAT...")
        if obb.account.login(pat=pat, remember_me=True) is None:
            print("Login successful!")
            is_logged_in = True  # Set the flag to True after successful login
        else:
            print("Login failed with PAT:", pat)
    except Exception as e:
        print(f"Error during login: {e}")

def add_env_param(kwargs, key, env_var, cast_type=None, default=None):
    """Helper function to add environment variables to kwargs if set."""
    value = os.getenv(env_var, default)
    if value is not None:
        kwargs[key] = cast_type(value) if cast_type else value

# Main function
async def main(**kwargs):
    await login()  # Ensure login is called only once

    # Run the screener
    screener = obb.equity.screener(**kwargs)

    # Print warnings if any
    if screener.warnings is None:
        print("No warnings")
    else:
        print("Warnings:", screener.warnings)

    return screener.results

# FastAPI setup
app = FastAPI()

origins = [
    "https://pro.openbb.co",
    "https://excel.openbb.co",
    "http://localhost:1420",  # Add your local development URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT_PATH = Path(__file__).parent.resolve()

@app.get("/")
def read_root():
    return {"Info": "OpenBB Custom Backend for volume screening"}

@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Custom Backend"""
    return JSONResponse(
        content=json.load((Path(__file__).parent.resolve() / "widgets.json").open())
    )

@app.get("/screener_table")
async def screener_table(
    volume_min: int = Query(None, description="Minimum trading volume"),
    volume_max: int = Query(None, description="Maximum trading volume"),
    price_min: float = Query(None, description="Minimum stock price"),
    price_max: float = Query(None, description="Maximum stock price"),
    mktcap_min: int = Query(None, description="Minimum market capitalization"),
    mktcap_max: int = Query(None, description="Maximum market capitalization"),
    beta_min: float = Query(None, description="Minimum beta value"),
    beta_max: float = Query(None, description="Maximum beta value"),
    dividend_min: float = Query(None, description="Minimum dividend amount"),
    dividend_max: float = Query(None, description="Maximum dividend amount"),
    is_etf: bool = Query(None, description="Filter for ETFs only (True/False)"),
    is_active: bool = Query(None, description="Filter for active tickers only (True/False)"),
    sector: str = Query(None, description="Filter by sector"),
    industry: str = Query(None, description="Filter by industry"),
    country: str = Query(None, description="Filter by country (two-letter code)"),
    exchange: str = Query("nyse", description="Filter by exchange"),
    limit: int = Query(50000, description="Limit the number of results"),
    provider: str = Query("fmp", description="Data provider"),
):
    """Endpoint to get screener results"""
    try:
        # Build kwargs dynamically from query parameters
        kwargs = {
            "volume_min": volume_min,
            "volume_max": volume_max,
            "price_min": price_min,
            "price_max": price_max,
            "mktcap_min": mktcap_min,
            "mktcap_max": mktcap_max,
            "beta_min": beta_min,
            "beta_max": beta_max,
            "dividend_min": dividend_min,
            "dividend_max": dividend_max,
            "is_etf": is_etf,
            "is_active": is_active,
            "sector": sector,
            "industry": industry,
            "country": country,
            "exchange": exchange,
            "limit": limit,
            "provider": provider,
        }

        # Remove None values from kwargs
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        # Call the main function with the kwargs
        results = await main(**kwargs)

        # Check if results is a list
        if isinstance(results, list):
            # Ensure all items in the list are JSON serializable
            serialized_results = [
                item.dict() if hasattr(item, "dict") else item for item in results
            ]
            return JSONResponse(content={"results": serialized_results})
        else:
            return JSONResponse(content={"error": "Unexpected data format for results"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

