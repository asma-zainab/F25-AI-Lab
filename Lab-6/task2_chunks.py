import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
docs = {
    "handbook": """The student handbook explains how coursework should be completed and submitted. Students should read each assignment carefully and check the instructions before beginning. Every assignment has a due date shown on the learning portal. Students should keep a copy of their work and make sure the uploaded file opens correctly. Late assignments are not accepted unless the student has an approved medical excuse. Students who need extra time should contact the course instructor as early as possible and explain the reason for the request. An extension is not automatic, and the instructor must confirm the new deadline. Students should check the portal after submitting work to make sure the status says submitted. If the upload fails, they should save a screenshot and contact the support office. The handbook also recommends planning work across the week instead of waiting until the final evening. Group assignments should include the names of all group members. Students must use their own words and mention sources when they use information from books or websites. If an instruction is unclear, students should ask the instructor before the due date. These steps help students avoid missed submissions and understand the course rules.""",

    "it_help": """The university IT help desk assists students with account and computer problems. Students use their university username and password to sign in to the learning portal. If a password is forgotten, the student can choose the password reset option on the sign-in page. A reset link or verification code may be sent to the registered email address. Students should check that email account and follow the instructions on the screen. They should never share their password or verification code with another person. If the registered email address is no longer available, the student should contact the IT help desk for assistance. The help desk may ask for the student's university ID to confirm the account. Students who cannot access the portal should include a short description of the problem when requesting help. They can also mention the device and browser they are using. Before reporting a problem, students can check their internet connection and try refreshing the page. The help desk is available during university working hours. Requests sent outside those hours are usually answered on the next working day. Keeping account details private helps protect student information.""",

    "library": """The university library allows students to borrow books for study and research. Students should use their library card when borrowing a book and should check the return date written on the loan record. Books must be returned on or before that date so other students can use them. A student may renew a borrowed book before the due date if no other reader has reserved it. If another reader has placed a reservation, the renewal request may be refused. Students should handle library books carefully and return them in good condition. If a book is lost or damaged, the student should contact library staff to discuss the next steps. The library catalogue can be used to search for books by title, author, or subject. Students can ask staff for help if they cannot find a book on the shelves. Quiet study areas are provided for individual work, while group study rooms may be booked separately. Food and drinks should be kept away from library materials. The library website lists opening hours and any changes during holidays. Students are encouraged to return books on time and respect the needs of other readers."""
}
def word_spans(text):
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]
def windows(text, size=40, overlap=0, offset=0):
    if size <= 0:
        raise ValueError("Chunk size must be positive.")
    if overlap < 0 or overlap >= size:
        raise ValueError("Overlap must be between 0 and size - 1.")
    spans = word_spans(text)
    chunks = []
    step = size - overlap
    for start in range(0, len(spans), step):
        selected = spans[start:start + size]
        if not selected:
            break
        chunk_start = selected[0][0]
        chunk_end = selected[-1][1]
        chunks.append({
            "start": offset + chunk_start,
            "end": offset + chunk_end,
            "text": text[chunk_start:chunk_end]
        })
    return chunks
def sentence_chunks(text, size=40):
    sentences = []
    for match in re.finditer(r"[^.!?]+[.!?]?", text):
        sentence = match.group()
        sentence_start = match.start()
        left = len(sentence) - len(sentence.lstrip())
        sentence = sentence.strip()
        sentence_start += left
        if sentence:
            sentences.append((sentence, sentence_start))
    chunks = []
    current_start = None
    current_end = None
    current_words = 0
    for sentence, sentence_start in sentences:
        count = len(word_spans(sentence))
        if count > size:
            if current_start is not None:
                chunks.append({
                    "start": current_start,
                    "end": current_end,
                    "text": text[current_start:current_end]
                })
                current_start = None
                current_end = None
                current_words = 0
            chunks.extend(windows(sentence, size, 0, sentence_start))
            continue
        if current_words + count <= size:
            if current_start is None:
                current_start = sentence_start
            current_end = sentence_start + len(sentence)
            current_words += count
        else:
            chunks.append({
                "start": current_start,
                "end": current_end,
                "text": text[current_start:current_end]
            })
            current_start = sentence_start
            current_end = sentence_start + len(sentence)
            current_words = count
    if current_start is not None:
        chunks.append({
            "start": current_start,
            "end": current_end,
            "text": text[current_start:current_end]
        })
    return chunks
def make_chunks(text, source, method):
    if method == "overlap_0":
        parts = windows(text, 40, 0)
    elif method == "overlap_10":
        parts = windows(text, 40, 10)
    elif method == "sentence":
        parts = sentence_chunks(text, 40)
    else:
        raise ValueError("Unknown chunking method.")
    records = []
    for i, part in enumerate(parts):
        records.append({
            "id": source + "_" + method + "_" + str(i + 1),
            "source": source,
            "start": part["start"],
            "end": part["end"],
            "text": part["text"]
        })
    return records
methods = ["overlap_0", "overlap_10", "sentence"]
all_records = {}
print("DOCUMENT WORD COUNTS")
for source, text in docs.items():
    print(source, ":", len(word_spans(text)), "words")
print("\nCHUNKING COMPARISON")
for method in methods:
    all_records[method] = []
    print("\nMethod:", method)
    for source, text in docs.items():
        chunks = make_chunks(text, source, method)
        all_records[method].extend(chunks)
        original_words = len(word_spans(text))
        chunk_words = sum(len(word_spans(c["text"])) for c in chunks)
        print("\nDocument:", source)
        print("Chunk count:", len(chunks))
        print("Chunk sizes:",
              [len(word_spans(c["text"])) for c in chunks])
        print("Repeated words:", chunk_words - original_words)
        for chunk in chunks:
            print(chunk["id"], chunk["start"], chunk["end"])
evidence = {
    "handbook": "Late assignments are not accepted unless the student has an approved medical excuse.",
    "it_help": "If a password is forgotten, the student can choose the password reset option on the sign-in page.",
    "library": "A student may renew a borrowed book before the due date if no other reader has reserved it."
}
print("\nRULE AND EXCEPTION CHECK")
for method in methods:
    print("\nMethod:", method)
    for source, rule in evidence.items():
        found = any(
            chunk["source"] == source and rule in chunk["text"]
            for chunk in all_records[method]
        )
        print(source, ":", "FOUND IN ONE CHUNK" if found else "NOT IN ONE CHUNK")
print("\nEDGE CASE TESTS")
print("Empty text:", windows("", 40, 0))
short_text = "This is a short document."
print("Short text:", windows(short_text, 40, 0))
try:
    windows("This is a test.", 40, 40)
except ValueError as error:
    print("Invalid overlap:", error)
long_sentence = " ".join(["student"] * 50) + "."
long_chunks = sentence_chunks(long_sentence, 40)
print("Long sentence chunk sizes:",
      [len(word_spans(c["text"])) for c in long_chunks])
print("\nTF-IDF SEARCH TEST")
search_records = all_records["sentence"]
queries = [
    "How can I get more time for my assignment?",
    "I cannot sign in because I forgot my password.",
    "Can I keep a borrowed book for a longer time?"
]
passages = [record["text"] for record in search_records]
vectorizer = TfidfVectorizer()
document_vectors = vectorizer.fit_transform(passages)
for query in queries:
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, document_vectors)[0]
    print("\nQuery:", query)
    top_indices = scores.argsort()[::-1][:3]
    for index in top_indices:
        record = search_records[index]
        print("\nChunk ID:", record["id"])
        print("Source:", record["source"])
        print("Score:", round(float(scores[index]), 3))
        print("Original offsets:", record["start"], "-", record["end"])
        print("Evidence:", record["text"])