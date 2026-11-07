from guided_chatbot import build_bot
engine = build_bot("embedding")
query = "assignment upload"
print("Suggested questions:")
for record, score in engine.search(query, k=3):
    print(
        record["question"],
        f"({score:.3f})"
    )