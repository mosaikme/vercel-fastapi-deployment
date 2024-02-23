from time import time
from fastapi import FastAPI, __version__
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import yfinance as yf
import pandas as pd
import numpy as np 


app = FastAPI()
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
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)
    
@app.get("/GETyf")
async def GETyf():
    df = yf.download("AAPL")
    df = df.to_dict()
    
    return{'res': 'pong', 'version': __version__, , df "time": time()}
    
@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}
