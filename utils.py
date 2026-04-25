from groq import Groq
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ──────────────────────────────────────────────
# LLM CALL — with retry
# ──────────────────────────────────────────────
def call_llm(prompt: str, retries: int = 2, temperature: float = 0.3) -> str:
    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt < retries:
                time.sleep(1.5)
            else:
                raise e


# ──────────────────────────────────────────────
# CLEAN LLM OUTPUT  (strips markdown fences)
# ──────────────────────────────────────────────
def clean_json_output(result: str) -> str:
    result = result.strip()
    if result.startswith("```"):
        lines = result.split("\n")
        # drop first (```json) and last (```) fence lines
        inner = [l for l in lines if not l.strip().startswith("```")]
        result = "\n".join(inner)
    return result.strip()


# ──────────────────────────────────────────────
# JD PARSER
# ──────────────────────────────────────────────
def parse_jd(prompt_template: str, jd_text: str) -> dict | None:
    prompt = prompt_template.format(jd=jd_text)
    result = call_llm(prompt)
    try:
        result = clean_json_output(result)
        data = json.loads(result)
        if isinstance(data, list):
            data = data[0]
        return {
            "skills":     data.get("skills", []),
            "experience": int(data.get("experience", 0)),
            "role":       data.get("role", ""),
        }
    except Exception:
        print("JD PARSE ERROR:", result)
        return None


# ──────────────────────────────────────────────
# ROLE MATCH
# ──────────────────────────────────────────────
def role_match(prompt_template: str, job_role: str, candidate_role: str) -> dict:
    prompt = prompt_template.format(job_role=job_role, candidate_role=candidate_role)
    result = call_llm(prompt)
    try:
        result = clean_json_output(result)
        data = json.loads(result)
        if isinstance(data, list):
            data = data[0]
        return {
            "score":  float(data.get("score", 0.5)),
            "reason": data.get("reason", "Role assessment unavailable."),
        }
    except Exception:
        print("ROLE MATCH ERROR:", result)
        return {"score": 0.5, "reason": "Could not assess role fit."}


# ──────────────────────────────────────────────
# SIMULATE CANDIDATE RESPONSE
# ──────────────────────────────────────────────
def simulate_response(prompt_template: str, job: str, skills: list, experience: int) -> str:
    prompt = prompt_template.format(
        job=job,
        skills=", ".join(skills),
        experience=experience,
    )
    # Higher temperature for more natural variation
    return call_llm(prompt, temperature=0.8)


# ──────────────────────────────────────────────
# INTEREST CLASSIFIER
# ──────────────────────────────────────────────
def classify_interest(prompt_template: str, response_text: str) -> dict:
    prompt = prompt_template.format(response=response_text)
    result = call_llm(prompt)
    try:
        result = clean_json_output(result)
        data = json.loads(result)
        if isinstance(data, list):
            data = data[0]
        return {
            "interest": data.get("interest", "Medium"),
            "score":    float(data.get("score", 0.5)),
        }
    except Exception:
        print("INTEREST ERROR:", result)
        return {"interest": "Medium", "score": 0.5}


# ──────────────────────────────────────────────
# SCORING FUNCTIONS
# ──────────────────────────────────────────────
def skill_match(jd_skills: list, candidate_skills: list) -> float:
    """Jaccard-style match: overlap / JD skills count."""
    if not jd_skills:
        return 1.0
    jd_set  = {s.lower().strip() for s in jd_skills}
    can_set = {s.lower().strip() for s in candidate_skills}
    return len(jd_set & can_set) / len(jd_set)


def experience_score(required: int, actual: int) -> float:
    """
    Smooth decay: full marks if actual >= required,
    penalty if under, smaller penalty if over.
    """
    if required == 0:
        return 1.0
    if actual >= required:
        # Slightly reward being over by up to 2 years, cap at 1.0
        return min(1.0, 1.0 + (actual - required) * 0.05)
    # Penalise being under: each missing year costs ~25%
    gap = required - actual
    return max(0.0, 1.0 - gap * 0.25)


def final_score(match: float, interest: float) -> float:
    """Weighted combination of match and interest scores."""
    return round(match * 0.7 + interest * 0.3, 4)
