import json
import requests
import yfinance as yf

def get_company_tickers():
  """Downloads and parses the stock ticker symbols from the GitHub-hosted SEC company tickers JSON file

  Returns:
    dict: A dictionary containing company tickers and related information.

    Notes:
      The data is sourced from the official SEC website via a GitHub respository:
      https://raw.githubusercontent.com/team-headstart/Financial-Analysis-and-Automation-with-LLMs/main/company_tickers.json

  """
  #URL to fetch the raw JSON file from Github
  url = "https://raw.githubusercontent.com/team-headstart/Financial-Analysis-and-Automation-with-LLMs/main/company_tickers.json"
  #Making a GET request to the URL
  response = requests.get(url)

  if response.status_code == 200:
      #Parse the Json content directly
      company_tickers = json.loads(response.content.decode('utf-8'))

      #Optionally save the content to a local file for future use
      with open("company_tickers.json", 'w',encoding='utf-8') as file:#create a json file
        json.dump(company_tickers, file, indent=4)#writes to the file

      print("File downloaded successfully and save as 'company_tickers.json")
      return company_tickers
  else:
      print(f"Failed to download file. Status code: response.status_code")
      return None
# company_tickers = get_company_tickers()