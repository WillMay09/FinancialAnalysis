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
from stockTickers import get_company_tickers
from embeddings import retrieve_matching_data
from groq import Client
from prompt import llm_taylored_prompt
client = Client(api_key=st.secrets["GROQ_API_KEY"])



st.title("Custom Stock Search")



#intialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []#empty list
#Display chat message from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


st.write("""Please enter your query below. This app specializes in retreiving
information on stocks.  If you are looking for information on a specific stock or industry, you are in the right place""")


prompt = st.chat_input("Ask me anything") 
if prompt:
      # Add user message to session history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder=st.empty()
        assistant_response = ""
        augmented_query = retrieve_matching_data(prompt)
        # Define the system prompt
        system_prompt = llm_taylored_prompt
        messages = [{"role": "system", "content": system_prompt},
        {"role": "user", "content": augmented_query},]
        messages.extend({"role": m["role"], "content": m["content"]} for m in st.session_state.messages)

        #parse in chunks
        for response in client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages,
             stream=True,  # Ensure streaming is set to True for chunks
        ):
            
            if hasattr(response, 'choices') and len(response.choices) > 0:
                content = response.choices[0].delta.content
                if content: 
                    assistant_response += content
                    message_placeholder.markdown(assistant_response+ " ")
            #message_placeholder.markdown(assistant_response)
        
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})