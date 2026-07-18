import os
from dotenv import load_dotenv
import anthropic
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_docs(docs_folder: str="docs"):
    """ Read all .md files from the docs folder into memory """
    path = Path(__file__).parent.parent / docs_folder
    result = {}
    for docs in path.glob("*.md"):
        result[docs.name] = docs.read_text()
    return result

def retrieve_relevant_doc(question: str, docs:list):
    """ Find the doc most relevant to the question using vectors """
    relevant_doc = None

    # convert values and question to vectors
    doc_texts = list(docs.values())
    doc_vectors = model.encode(doc_texts)
    question_vector = model.encode(question)

    # rank similiarites and return best score
    scores = util.cos_sim(question_vector, doc_vectors)
    best_index = scores.argmax().item()
    relevant_doc = doc_texts[best_index]

    return relevant_doc

def ask_claude(question: str, context:str) -> str:
    """ Send the question + retrieve from claude, return answer """
    system_prompt = f"You are an MTG rules assistant. Use this context to answer:\n\n{context}"

    response = client.messages.create(
        model = "claude-sonnet-5",
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": question}]
    )
    for block in response.content:
        if block.type == "text":
            return block.text

def main():
    """ load docs, retrieve, ask, print"""
    docs = load_docs()
    print("I am the MTG rules assistant, please ask me a MTG commander-related question.\n")
    while True:
        user_input = input()
        relevant_doc = retrieve_relevant_doc(user_input, docs)
        answer = ask_claude(user_input, relevant_doc)
        print(answer)

if __name__ == "__main__":
    main()

