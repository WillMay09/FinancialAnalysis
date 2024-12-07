import concurrent
from langchain.schema import Document
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from main import get_stock_info
from stockTickers import get_company_tickers
import streamlit as st
import yfinance as yf
import time
from main import yahoo_tickers
pinecone_api_key = st.secrets["PINECONE_API_KEY"]


index_name = "stocks"
namespace = "stock-descriptions"
hf_embeddings = "stock-descriptions"

hf_embeddings = HuggingFaceEmbeddings()
vectorstore = PineconeVectorStore(index_name=index_name, embedding=hf_embeddings)

#Initialize tracking lists

successful_tickers = []#2 lists to track successful and unsuccessful tickers
unsuccessful_tickers = []

#load existing successful/unsuccessful tickers
try:
  with open('successful_tickers.txt', 'r') as f:
    successful_tickers = [line.strip() for line in f if line.strip()]#stripes line of whitespace and then loads the successful tickers
    print(f"Loaded {len(successful_tickers)} successful tickers")#prints the number of successful tickers
except FileNotFoundError:#if the file is does not exist throw an error
  print("No existing successful tickers file found")

try:
  with open('unsuccessful_tickers.txt', 'r') as f:
    unsuccessful_tickers = [line.strip() for line in f if line.strip()]
  print(f"Loaded {len(unsuccessful_tickers)} unsuccessful tickers")
except FileNotFoundError:
  print("No existing unsuccessful tickers file found")

def process_stock(stock_ticker: str) -> str:
# Skip if already processed
    if stock_ticker in successful_tickers:
        return f"Already processed {stock_ticker}"

    try:
        # Get and store stock data
        stock_data = get_stock_info(stock_ticker)
        stock_description = stock_data['Business Summary']

        # Store stock description in Pinecone
        vectorstore_from_texts = PineconeVectorStore.from_documents(
            documents=[Document(page_content=stock_description, metadata=stock_data)],
            embedding=hf_embeddings,
            index_name=index_name,
            namespace=namespace
        )
        time.sleep(5)
        # Track success
        with open('successful_tickers.txt', 'a') as f:
            f.write(f"{stock_ticker}\n")
        successful_tickers.append(stock_ticker)

        return f"Processed {stock_ticker} successfully"

    except Exception as e:
        # Track failure
        with open('unsuccessful_tickers.txt', 'a') as f:
            f.write(f"{stock_ticker}\n")
        unsuccessful_tickers.append(stock_ticker)

        return f"ERROR processing {stock_ticker}: {e}"

def parallel_process_stocks(tickers: list, max_workers: int = 10) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ticker = {
            executor.submit(process_stock, ticker): ticker
            for ticker in tickers
        }

        for future in concurrent.futures.as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                result = future.result()
                print(result)

                # Stop on error
                if result.startswith("ERROR"):
                    print(f"Stopping program due to error in {ticker}")
                    executor.shutdown(wait=False)
                    raise SystemExit(1)

            except Exception as exc:
                print(f'{ticker} generated an exception: {exc}')
                print("Stopping program due to exception")
                executor.shutdown(wait=False)
                raise SystemExit(1)

# Prepare your tickers
tickers_to_process = [yahoo_tickers[num]['ticker'] for num in yahoo_tickers.keys()]

# Process them
parallel_process_stocks(tickers_to_process, max_workers=15)
# for idx, stock in yahoo_tickers.items():
#     stock_ticker = stock['ticker']

#     try:
#         stock_data = get_stock_info(stock_ticker)
#         stock_description = stock_data['Business Summary'] if stock_data['Business Summary'] != 'Information not available' else 'No description available'

#         print(f"Processing stock {idx} / {len(yahoo_tickers) - 1}: {stock_ticker}",end="\r")

#         vectorstore_from_documents = PineconeVectorStore.from_documents(
#             documents=[Document(page_content=stock_description, metadata=stock_data)],
#             embedding=hf_embeddings,
#             index_name=index_name,
#             namespace=namespace
#         )

#         print(f"Successfully processed stock {idx} / {len(yahoo_tickers) - 1}: {stock_ticker}")
        
#         with open("successful_tickers.txt", "a") as success_file:
#             success_file.write(f"{stock_ticker}\n")
#     except Exception as e:
#         print(f"Error processing stock {idx} / {len(yahoo_tickers) - 1} ({stock_ticker}): {e}")
#         with open("unsuccessful_tickers.txt", "a") as error_file:
#             error_file.write(f"{stock_ticker}\n")

#         if str(e) == "can't start new thread":
#             print("Stock processing failed due to thread limit. Terminating the process...")
#             break
        
#     if int(idx) and int(idx) % 500 == 0:
#         print("Sleeping for 2 minutes to avoid rate limiting...")
#         time.sleep(120)