import os
from dotenv import load_dotenv
import anthropic
from pathlib import Path

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def load_docs(docs_folder: str="docs"):
    """ Read all .md files from the docs folder into memory """
    path = Path(docs_folder)
    result = {}
    for docs in path.glob("*.md"):
        result[docs.name] = docs.read_text()
    return result

def retrieve_relevant_doc(question: str, docs:list):
    """ Find the doc most relevant to the question """
    relevant_doc = None
    for doc in docs:
        for keyword in question.split():
            if keyword in docs[doc]:
                relevant_doc = docs[doc]

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
    user_input = input()
    relevant_doc = retrieve_relevant_doc(user_input, docs)
    answer = ask_claude(user_input, relevant_doc)
    print(answer)

if __name__ == "__main__":
    main()

