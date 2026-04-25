import streamlit as st
import json
import pandas as pd
import io

from utils import *
from prompts import *

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Talent Scout",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    .stProgress > div > div > div > div { border-radius: 8px; }
    .metric-card {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin-bottom: 8px;
    }
    .metric-card h2 { margin: 0; font-size: 2rem; }
    .metric-card p  { margin: 0; color: #666; font-size: 0.85rem; }
    .tag {
        display: inline-block;
        background: #e8f0fe;
        color: #1a73e8;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.8rem;
        margin: 2px;
    }
    .tag-match {
        background: #e6f4ea;
        color: #137333;
    }
    .candidate-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        background: white;
    }
    .badge-high   { background:#e6f4ea; color:#137333; padding:2px 10px; border-radius:20px; font-size:0.8rem; }
    .badge-medium { background:#fef7e0; color:#b06000; padding:2px 10px; border-radius:20px; font-size:0.8rem; }
    .badge-low    { background:#fce8e6; color:#c5221f; padding:2px 10px; border-radius:20px; font-size:0.8rem; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# LOAD CANDIDATES
# ──────────────────────────────────────────────
with open("candidates.json") as f:
    candidates = json.load(f)

# ──────────────────────────────────────────────
# SIDEBAR — CONFIG & INFO
# ──────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4616/4616655.png", width=60)
    st.title("AI Talent Scout")
    st.caption("Powered by LLM-based matching & interest simulation")

    st.divider()
    st.subheader("⚙️ Scoring Weights")
    w_skill = st.slider("Skill Match Weight",       0.0, 1.0, 0.50, 0.05)
    w_exp   = st.slider("Experience Match Weight",  0.0, 1.0, 0.30, 0.05)
    w_role  = st.slider("Role Fit Weight",          0.0, 1.0, 0.20, 0.05)

    total = round(w_skill + w_exp + w_role, 2)
    if abs(total - 1.0) > 0.01:
        st.warning(f"Weights sum to {total}. Adjust to total 1.0 for best results.")
    else:
        st.success("Weights sum to 1.0 ✓")

    st.divider()
    st.subheader("📋 Candidate Pool")
    st.info(f"{len(candidates)} candidates loaded from `candidates.json`")
    if st.checkbox("Preview candidates"):
        for c in candidates:
            st.write(f"**{c['name']}** — {c['role']} ({c['experience']}y)")

    st.divider()
    st.caption("Built for Catalyst Hackathon · Deccan AI")

# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────
st.title("🎯 AI Talent Scout")
st.write("Paste a Job Description below. The agent parses it, scores every candidate on **match** and **simulated interest**, and ranks them for you.")

# ──────────────────────────────────────────────
# SAMPLE JDs  (must come BEFORE the text_area)
# ──────────────────────────────────────────────
SAMPLES = {
    "ML Engineer – Computer Vision": (
        "We are hiring an ML Engineer with expertise in Deep Learning, PyTorch, "
        "and Computer Vision. Minimum 4 years of experience. You will build and "
        "deploy models for real-time object detection at scale."
    ),
    "Backend Developer – Python/Django": (
        "Looking for a Backend Developer with 3+ years experience in Python, Django, "
        "PostgreSQL and REST APIs. You will design scalable microservices."
    ),
    "Data Scientist – NLP": (
        "Hiring a Data Scientist with strong NLP, Python, and Machine Learning skills. "
        "Experience with TensorFlow or PyTorch preferred. 2+ years experience."
    ),
    "Frontend Developer – React/TypeScript": (
        "We need a Frontend Developer skilled in React, TypeScript, Next.js and UI/UX. "
        "3 years minimum experience building responsive web applications."
    ),
}

with st.expander("📎 Load a sample JD"):
    sample = st.selectbox("Pick a sample", ["None"] + list(SAMPLES.keys()))
    if sample != "None":
        if st.button("Use this JD"):
            st.session_state["jd_text"] = SAMPLES[sample]
            st.rerun()

col_jd, col_tip = st.columns([3, 1])
with col_jd:
    jd = st.text_area(
        "📄 Job Description",
        value=st.session_state.get("jd_text", ""),
        height=160,
        placeholder="e.g. We are looking for a Python developer with 3+ years of experience in Django, PostgreSQL and REST APIs...",
        key="jd_text",
    )
with col_tip:
    st.markdown("**Tips:**")
    st.markdown("- Include required skills\n- Mention experience level\n- State the job title clearly")

# ──────────────────────────────────────────────
# ANALYSE BUTTON
# ──────────────────────────────────────────────
analyze = st.button("🚀 Analyse Candidates", type="primary", use_container_width=True)

if analyze:
    if not jd.strip():
        st.error("Please paste a Job Description first.")
        st.stop()

    with st.spinner("Step 1/4 — Parsing Job Description…"):
        jd_data = parse_jd(JD_PARSE_PROMPT, jd)

    if not jd_data:
        st.error("❌ JD parsing failed. Try again or simplify the JD text.")
        st.stop()

    # ── Show parsed JD summary ─────────────────
    with st.expander("🔍 Parsed JD", expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.metric("Role", jd_data["role"])
        c2.metric("Min Experience", f"{jd_data['experience']} yrs")
        c3.metric("Required Skills", len(jd_data["skills"]))
        st.write("**Skills extracted:** " + " ".join(
            f'<span class="tag">{s}</span>' for s in jd_data["skills"]
        ), unsafe_allow_html=True)

    results = []
    progress_bar = st.progress(0, text="Evaluating candidates…")

    for idx, c in enumerate(candidates):

        with st.spinner(f"Step 2–4 — Evaluating {c['name']}…"):

            skill_score = skill_match(jd_data["skills"], c["skills"])
            exp_score   = experience_score(jd_data["experience"], c["experience"])

            role_data = role_match(ROLE_MATCH_PROMPT, jd_data["role"], c["role"])

            match_score = (
                skill_score  * w_skill +
                exp_score    * w_exp   +
                role_data["score"] * w_role
            )

            matched_skills = list(set(jd_data["skills"]) & set(c["skills"]))
            missing_skills = list(set(jd_data["skills"]) - set(c["skills"]))

            response = simulate_response(
                OUTREACH_PROMPT, jd_data["role"], c["skills"], c["experience"]
            )
            interest_data = classify_interest(INTEREST_PROMPT, response)

            final = final_score(match_score, interest_data["score"])

            results.append({
                "name":           c["name"],
                "role":           c["role"],
                "experience":     c["experience"],
                "skills":         c["skills"],
                "match_score":    round(match_score, 3),
                "skill_score":    round(skill_score, 3),
                "exp_score":      round(exp_score, 3),
                "role_score":     round(role_data["score"], 3),
                "interest":       interest_data["interest"],
                "interest_score": round(interest_data["score"], 3),
                "final_score":    round(final, 3),
                "response":       response,
                "reason":         role_data["reason"],
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
            })

        progress_bar.progress((idx + 1) / len(candidates),
                              text=f"Evaluated {idx+1}/{len(candidates)} candidates")

    results = sorted(results, key=lambda x: x["final_score"], reverse=True)
    progress_bar.empty()

    # ── SUMMARY METRICS ───────────────────────
    st.divider()
    st.subheader("📊 Summary")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Candidates Evaluated", len(results))
    m2.metric("Top Candidate",        results[0]["name"])
    m3.metric("Top Score",            f"{results[0]['final_score']:.0%}")
    m4.metric("High Interest",        sum(1 for r in results if r["interest"] == "High"))

    # ── COMPARISON TABLE ──────────────────────
    st.divider()
    st.subheader("📋 Rankings Table")
    df = pd.DataFrame([{
        "Rank":           i + 1,
        "Name":           r["name"],
        "Current Role":   r["role"],
        "Exp (yrs)":      r["experience"],
        "Match Score":    f"{r['match_score']:.0%}",
        "Interest":       r["interest"],
        "Interest Score": f"{r['interest_score']:.0%}",
        "Final Score":    f"{r['final_score']:.0%}",
    } for i, r in enumerate(results)])
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ── EXPORT ────────────────────────────────
    csv_buf = io.StringIO()
    df.to_csv(csv_buf, index=False)
    st.download_button(
        "⬇️ Download CSV",
        csv_buf.getvalue(),
        file_name="talent_scout_results.csv",
        mime="text/csv",
    )

    # ── DETAILED CANDIDATE CARDS ──────────────
    st.divider()
    st.subheader("🧑‍💼 Candidate Profiles")

    for i, r in enumerate(results):

        interest_badge = {
            "High":   f'<span class="badge-high">🟢 High</span>',
            "Medium": f'<span class="badge-medium">🟡 Medium</span>',
            "Low":    f'<span class="badge-low">🔴 Low</span>',
        }.get(r["interest"], r["interest"])

        medal = {0: "🥇", 1: "🥈", 2: "🥉"}.get(i, f"#{i+1}")

        with st.expander(
            f"{medal} **{r['name']}** — Final Score: {r['final_score']:.0%} | Interest: {r['interest']}",
            expanded=(i == 0),
        ):
            left, right = st.columns([3, 2])

            with left:
                st.markdown(f"**Current Role:** {r['role']} &nbsp;|&nbsp; **Experience:** {r['experience']} years")
                st.markdown(f"**Interest Level:** {interest_badge}", unsafe_allow_html=True)

                # Skill tags
                matched_html = "".join(
                    f'<span class="tag tag-match">✓ {s}</span>' for s in r["matched_skills"]
                )
                missing_html = "".join(
                    f'<span class="tag">{s}</span>' for s in r["missing_skills"]
                )
                if matched_html:
                    st.markdown(f"**Matched Skills:** {matched_html}", unsafe_allow_html=True)
                if missing_html:
                    st.markdown(f"**Missing Skills:** {missing_html}", unsafe_allow_html=True)

                st.markdown(f"**Role Fit Reason:** _{r['reason']}_")

                st.markdown("**💬 Simulated Candidate Response:**")
                st.info(r["response"])

            with right:
                st.markdown("**Score Breakdown**")

                st.caption(f"Skill Match — {r['skill_score']:.0%}")
                st.progress(r["skill_score"])

                st.caption(f"Experience Fit — {r['exp_score']:.0%}")
                st.progress(r["exp_score"])

                st.caption(f"Role Fit — {r['role_score']:.0%}")
                st.progress(r["role_score"])

                st.caption(f"Match Score (weighted) — {r['match_score']:.0%}")
                st.progress(r["match_score"])

                st.caption(f"Interest Score — {r['interest_score']:.0%}")
                st.progress(r["interest_score"])

                st.markdown("---")
                st.metric("**Final Score**", f"{r['final_score']:.0%}")

    # ── TOP PICK CALLOUT ──────────────────────
    top = results[0]
    st.divider()
    st.success(
        f"🏆 **Recommended Hire: {top['name']}**  \n"
        f"Final Score **{top['final_score']:.0%}** | "
        f"Interest: **{top['interest']}** | "
        f"Matched Skills: {', '.join(top['matched_skills']) or 'None'}"
    )
