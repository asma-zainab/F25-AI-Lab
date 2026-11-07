import re
samples = [
    "These tasks are too difficult!", "I don't know.","what@gmail.com","SE2026", "", "اتنے سارے ٹاسک کیوں ہیں؟"]
for text in samples:
    whitespace = text.split()
    words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    print("\nOriginal:", repr(text))
    print("Whitespace:", whitespace, len(whitespace))
    print("Word-like:", words, len(words))
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2",
        device="cpu"
    )
    for text in samples[:2]:
        print("\nOriginal:", text)
        print("Model tokens:", model.tokenizer.tokenize(text))
except Exception as error:
    print("\nModel tokenizer unavailable:", error)