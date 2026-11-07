import numpy as np
from sentence_transformers import SentenceTransformer
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device="cpu"
)
passages = [
    "Students can reset their password through the university portal.",
    "Assignments must be uploaded before the submission deadline.",
    "Students can contact the IT helpdesk for login problems."
]
C = model.encode(passages, normalize_embeddings=True)
Q = model.encode(
    ["How can I recover my login?"],
    normalize_embeddings=True
)
scores = (Q @ C.T)[0]
print("Embedding shape:", C.shape)
for i in np.argsort(-scores):
    print(i, round(float(scores[i]), 3), passages[i])
assert np.allclose(
    np.linalg.norm(C, axis=1),
    1,
    atol=1e-5
)