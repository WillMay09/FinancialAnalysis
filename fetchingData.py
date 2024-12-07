import numpy as np
from sentence_transformers import SentenceTransformer
from torch import cosine_similarity

from stockTickers import get_company_tickers




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
        'Business Summary': stock_info.get('longBusinessSummary', 'Information not available'),
        'City': stock_info.get('city', 'Information not available'),
        'State': stock_info.get('state', 'Information not available'),
        'Country': stock_info.get('country', 'Information not available'),
        'Industry': stock_info.get('industry', 'Information not available'),
        'Sector': stock_info.get('sector', 'Information not available')
    }

    return properties

# data = yf.Ticker("NVDA")#grab nvidea stock
# stock_info = data.info
# print(stock_info)

def get_huggingface_embeddings(text, model_name="sentence-transformers/all-mpnet-base-v2"):
    """
    Generates embeddings for the given text using the specified Hugging Face model.

    Args:
          text (str): The input text to generate embeddings for.
          model_name (str): The name of the Hugging Face model to use.
                            Defaults to "sentence-transformers/all-mpnet-base-v2".

      Returns:
          np.ndarray: The generated embeddings as a NumPy array.
      """
    model = SentenceTransformer(model_name)

    return model.encode(text)

def cosine_similarity_between_sentences(sentence1, sentence2):#how similiar two vectors are
    """
    Calculates the cosine similarity between two sentences.

    Args:
        sentence1 (str): The first sentence for comparision.
        sentence2 (str): The second sentence.

    Returns:
        float: The cosine similarity between the two sentences.

    Notes: Prints the similarity score to the console in a formatted string.


    """
    #Get embeddings for both sentences
    embedding1 = np.array(get_huggingface_embeddings(sentence1))#embeddings are converted into NumPy arrays for computation
    embedding2 = np.array(get_huggingface_embeddings(sentence2))

    #Reshape embeddings into 2d array for cosine_similarity function
    embedding1 = embedding1.reshape(1, -1)
    embedding2 = embedding2.reshape(1, -1)

    #Calculate cosine similarity
    similarity = cosine_similarity(embedding1, embedding2)
    similarity_score = similarity[0][0]
    print(f"Similarity Score: {similarity_score:.4f}")
    return similarity_score

sentence1 = "Hello there, I am obi-wan kenobi"
sentence2 = "Hello master, I am anakin skywalker"

# similarity = cosine_similarity_between_sentences(sentence1, sentence2)
# print(similarity)

yahoo_tickers = get_company_tickers()