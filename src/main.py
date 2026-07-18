import os
from dotenv import load_dotenv
import anthropic
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import requests

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

def fetch_scryfall(question):
    """ Extract a card name from the question and fetch its data from Scryfall """
    # Ask Claude to extract just the card name
    extraction = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=50,
        messages=[{"role": "user", "content": f"Extract just the MTG card name from this question. Reply with only the card name, nothing else: {question}"}]
    )
    card_name = None
    for block in extraction.content:
        if block.type == "text":
            card_name = block.text.strip()
            break

    if not card_name:
        return ""

    response = requests.get(
        "https://api.scryfall.com/cards/named",
        params={"fuzzy": card_name},
        headers={"User-Agent": "mtg-rules-assistant/1.0"}
    )

    if response.status_code != 200:
        return ""

    card = response.json()
    return f"Card: {card.get('name', '')}\n{card.get('oracle_text', '')}"

def retrieve_relevant_doc(question: str, docs:list, doc_vectors):
    """ Find the doc most relevant to the question using vectors """
    relevant_doc = None
    doc_texts = list(docs.values())
    # convert question to vectors
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
    return ""



