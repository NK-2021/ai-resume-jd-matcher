from __future__ import annotations
from sentence_transformers import SentenceTransformer
import numpy as np

_MODEL = None

def _get_model() -> SentenceTransformer:
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-9
    return float(np.dot(a, b) / denom)


def score_resume_vs_jd(resume_text: str, jd_text: str) -> dict:
    """
    Returns stable, explainable similarity scores (0..100).
    """
    model = _get_model()

    resume = resume_text.strip()
    jd = jd_text.strip()

    emb = model.encode([resume, jd], normalize_embeddings=True)
    overall = cosine_sim(emb[0], emb[1])

    # convert to 0..100
    overall_pct = int(round(max(0.0, min(1.0, overall)) * 100))

    return {
        "overall_similarity": overall,
        "overall_pct": overall_pct
    }
