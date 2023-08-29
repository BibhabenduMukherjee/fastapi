from fastapi import FastAPI
import os
from dotenv import load_dotenv, dotenv_values
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
import qdrant_client
load_dotenv()
from langchain.llms import OpenAI
from pydantic import BaseModel
from langchain.chains import RetrievalQA
# create the client


# Create an instance of the FastAPI class
app = FastAPI()
#openai_api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings()
client = qdrant_client.QdrantClient(
    os.getenv("QDRANT_HOST"),
    api_key=os.getenv("QDRANT_API_KEY")
)

vectorstore = Qdrant(
    client=client,
    collection_name=os.getenv("QDRANT_COLLECTION"),
    embeddings=embeddings
)

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
    )

# query = "i am worried is the system secure"
# response = qa.run(query)

@app.get("/", tags=["Root"])
async def read_root():
    return {"Hello": "World"}


class QueryRequest(BaseModel):
    query: str


@app.post("/qt")
async def process_query(query_request: QueryRequest):
    query = query_request.query
    # Do something with the query, for example, print it
    response_llm = qa.run(query)
    print("Received query:", query)

    # You can perform any processing here and return a response
    response = {"answer": response_llm}
    return response
