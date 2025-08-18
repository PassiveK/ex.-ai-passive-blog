import os, requests, pandas as pd, datetime

topics = pd.read_csv("generator/topics.csv")
topic = topics.sample(1).iloc[0]["topic"]

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "google/gemma-2-2b-it")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

prompt = f"Ecris un article de blog SEO optimisé sur : {topic}"
response = requests.post(
    f"https://api-inference.huggingface.co/models/{HF_MODEL_ID}",
    headers=headers, json={"inputs": prompt}
)
text = response.json()[0]["generated_text"] if isinstance(response.json(), list) else str(response.json())

today = datetime.date.today().isoformat()
os.makedirs("docs", exist_ok=True)
with open(f"docs/{today}.md", "w") as f:
    f.write(f"# {topic}\n\n{text}")

with open("docs/index.md", "a") as idx:
    idx.write(f"- [{topic}]({today}.html)\n")
