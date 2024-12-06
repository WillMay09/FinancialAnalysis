import streamlit as st
from langchain_pinecone import PineconeVectorStore
from openai import OpenAI
import dotenv
import json
import yfinance as yf
import concurrent.futures
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import numpy as np
import requests
import os

def get_stock_info(symbol: str) -> dict:
    """Retrieves and formats detailed information about a given stock from Yahoo Finance.

    Args: symbol(str): The stock ticker symbol to look up

    Returns:
    dict: A dictionary containing detailed stock information, including ticker, name, business summary, city, state, country, industry, and sector"""
    data = yf.Ticker(symbol)
    stock_info = data.info

    properties = {
        "Ticker": stock_info.get('symbol', 'Information not available'),
        'Name': stock_info.get('longName', 'Information not available'),
        'Bussiness Summary': stock_info.get('longBusinessSummary', 'Information not available'),
        'City': stock_info.get('city', 'Information not available'),
        'State': stock_info.get('state', 'Information not available'),
        'Country': stock_info.get('country', 'Information not available'),
        'Industry': stock_info.get('industry', 'Information not available'),
        'Sector': stock_info.get('sector', 'Information not available')
    }

    return properties

data = yf.Ticker("NVDA")#grab nvidea stock
stock_info = data.info
print(stock_info)