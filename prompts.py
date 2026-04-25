# ──────────────────────────────────────────────
# JD PARSER PROMPT
# ──────────────────────────────────────────────
JD_PARSE_PROMPT = """
You are a recruitment assistant. Extract structured data from the job description below.

Return ONLY a valid JSON object with exactly these keys:
{{
  "skills": ["skill1", "skill2"],
  "experience": 0,
  "role": "short job title"
}}

Rules:
- "skills": list of specific technical skills, tools, or languages mentioned (max 8)
- "experience": minimum years required as an integer (0 if not specified)
- "role": short job title (2–4 words max)
- No markdown, no explanation, no extra text — JSON only

Job Description:
{jd}
"""


# ──────────────────────────────────────────────
# ROLE MATCH PROMPT
# ──────────────────────────────────────────────
ROLE_MATCH_PROMPT = """
You are a senior recruiter evaluating role fit.

Job requires: {job_role}
Candidate's current role: {candidate_role}

Score how well the candidate's role aligns with the job role.

Return ONLY valid JSON:
{{
  "score": 0.85,
  "reason": "One sentence explanation of fit or gap"
}}

Rules:
- score: float 0.0–1.0 (1.0 = perfect match, 0.0 = completely unrelated)
- reason: exactly one sentence, specific to these roles
- No markdown, no extra text — JSON only
"""


# ──────────────────────────────────────────────
# OUTREACH PROMPT
# ──────────────────────────────────────────────
OUTREACH_PROMPT = """
You are a job candidate receiving a recruiter message.

Your profile:
- Current role: {job}
- Skills: {skills}
- Years of experience: {experience}

Recruiter's message:
"Hi! We have an exciting opportunity that might be a great fit for your profile. Are you open to a quick chat about it?"

Write a realistic, natural reply. Your response should:
- Reflect your personality and confidence level (more experience = more selective)
- Be genuine, not robotic
- Be 1–3 sentences only
- Vary each time — don't always say yes or no

Reply (just your response, no name/greeting needed):
"""


# ──────────────────────────────────────────────
# INTEREST CLASSIFICATION PROMPT
# ──────────────────────────────────────────────
INTEREST_PROMPT = """
Classify the candidate's interest level from their reply to a recruiter.

Candidate reply:
{response}

Rules:
- High   (score 0.75–1.0): clearly enthusiastic, eager to learn more, asks questions
- Medium (score 0.40–0.74): curious but cautious, open but non-committal
- Low    (score 0.00–0.39): disinterested, busy, passively declining, or rejecting

Return ONLY valid JSON:
{{
  "interest": "High",
  "score": 0.85
}}

No markdown, no explanation — JSON only.
"""
