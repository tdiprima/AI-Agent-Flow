import os
from datetime import datetime, timezone

import requests
from langchain.chains import ConversationalRetrievalChain
from langchain.docstore.document import Document
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI, OpenAIEmbeddings

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def fetch_weather_forecast(city, api_key):
    """
    Fetch Weather Data from OpenWeatherMap
    Get the 5-day forecast for a city
    """
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
    resp = requests.get(url)
    data = resp.json()
    return data["list"]


def store_forecasts_in_faiss(forecasts, city):
    """
    Store Forecasts in FAISS Vector Store
    Each forecast entry is treated as a document. We'll use LangChain's FAISS wrapper.
    """
    docs = []
    for forecast in forecasts:
        # dt = datetime.utcfromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M')  # Deprecated in Python 3.12
        dt = datetime.fromtimestamp(forecast["dt"], tz=timezone.utc).strftime(
            "%Y-%m-%d %H:%M"
        )
        temp = forecast["main"]["temp"]
        weather = forecast["weather"][0]["description"]
        doc = Document(
            page_content=f"Date: {dt}, City: {city}, Temp: {temp}°C, Weather: {weather}",
            metadata={"date": dt, "city": city},
        )
        docs.append(doc)
    embeddings = OpenAIEmbeddings()
    vectordb = FAISS.from_documents(docs, embeddings)
    return vectordb


def build_agent(vectordb):
    """
    Create a RetrievalQA Chain with Memory
    We'll use LangChain's RetrievalQA with memory to allow multi-step queries.
    """
    retriever = vectordb.as_retriever()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = OpenAI(temperature=0)
    qa = ConversationalRetrievalChain.from_llm(llm, retriever, memory=memory)
    return qa


if __name__ == "__main__":
    city = "London"
    forecasts = fetch_weather_forecast(city, OPENWEATHER_API_KEY)
    vectordb = store_forecasts_in_faiss(forecasts, city)
    agent = build_agent(vectordb)

    # Example multi-step query
    query = "What's the forecast trend for next week? Is it getting warmer or colder?"
    result = agent.invoke({"question": query})
    print(result)

    # Follow-up question
    followup = "What about the chance of rain?"
    result2 = agent.invoke({"question": followup})
    print(result2)
