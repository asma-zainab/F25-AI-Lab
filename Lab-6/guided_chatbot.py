from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
faqs = [
    {
        "question": "How can I reset my password?",
        "answer": "You can reset your password using the password reset option on the sign-in page.",
        "source": "IT Help Guide"
    },
    {
        "question": "When should I submit my assignment?",
        "answer": "You should submit your assignment before the given deadline.",
        "source": "Student Guide"
    }
]
class Chatbot:

    def __init__(self):
        self.questions = [faq["question"] for faq in faqs]

        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(
            self.questions
        )
    def search(self, user_input):
        if user_input.strip() == "":
            return "Please enter a question."
        for faq in faqs:
            if user_input.lower().strip() == faq["question"].lower():
                return (
                    faq["answer"] +
                    "\nSource: " + faq["source"]
                )
        user_vector = self.vectorizer.transform([user_input])
        scores = cosine_similarity(
            user_vector,
            self.question_vectors
        )[0]
        best_index = scores.argmax()
        best_score = scores[best_index]
        if best_score >= 0.15:
            faq = faqs[best_index]
            return (
                "Did you mean: " + faq["question"] +
                "\nAnswer: " + faq["answer"] +
                "\nSource: " + faq["source"]
            )
        return "Sorry, I could not find a relevant answer."
def build_bot():
    return Chatbot()
bot = build_bot()
print("Student Help Chatbot")
print("Type 'exit' to close the chatbot.")
while True:
    user_input = input("\nYou: ")
    if user_input.lower().strip() == "exit":
        print("Chatbot closed.")
        break
    response = bot.search(user_input)
    print("Chatbot:", response)