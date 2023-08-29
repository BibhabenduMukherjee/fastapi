import os
from dotenv import load_dotenv, dotenv_values
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
load_dotenv()
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
import qdrant_client

# create the client
client = qdrant_client.QdrantClient(
    os.getenv("QDRANT_HOST"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# create the collection
collection_config = qdrant_client.http.models.VectorParams(
    size=1536,  # 768 for instructor-xl, 1536 for OpenAI
    distance=qdrant_client.http.models.Distance.COSINE
)

client.recreate_collection(
    collection_name=os.getenv("QDRANT_COLLECTION"),
    vectors_config=collection_config
)

embeddings = OpenAIEmbeddings()

vectorstore = Qdrant(
    client=client,
    collection_name=os.getenv("QDRANT_COLLECTION"),
    embeddings=embeddings
)

import pickle



def get_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


with open("test/story.txt") as f:
    raw_text = f.read()

texts = get_chunks(raw_text)

vectorstore.add_texts(texts)




# qa = RetrievalQA.from_chain_type(
#     llm=OpenAI(),
#     chain_type="stuff",
#     retriever=vectorstore.as_retriever()
#     )
#
# query = "i am worried is the system secure"
# response = qa.run(query)
#
# print(response)