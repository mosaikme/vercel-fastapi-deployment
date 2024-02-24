from time import time
from fastapi import FastAPI, __version__
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import yfinance as yf
import pandas as pd
import numpy as np 



# ==================================================================
# Cache
# ==================================================================
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder
from contextlib import asynccontextmanager


    


@asynccontextmanager
async def lifespan(app: FastAPI):
    ##This is StartUp

    # Initialise the Client on startup and add it to the state
    FastAPICache.init(InMemoryBackend())
    # websocket_task = asyncio.create_task(start_websocket())

    yield
    
app = FastAPI(docs_url=None, redoc_url=None ,lifespan=lifespan)  
app.mount("/static", StaticFiles(directory="static"), name="static")


    
html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI@{__version__}</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
                <li><a href="/GETyf">/GETyf</a></li>
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)
    
@cache(expire=60*30,namespace='abc',coder=PickleCoder) ## choosing coder pickle to store DATAFRAMES.
async def get_stock_data(symbols):
    # Fetch historical data using yfinance for all symbols
    data = yf.download(symbols)
    print("CHACHE IT ")
    return data

@app.get("/GETyf")
async def GETyf():
    start_time= time()
    df = await get_stock_data("AAPL")
    # df = yf.download("AAPL")
    df = df.to_dict()
    send_time = time() - start_time 
    return{'res': 'pongsss', 'version': __version__ , "time": time() ,"send_time":send_time,"df" : df}
    
@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}
