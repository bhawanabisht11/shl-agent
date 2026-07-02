from rag.retriever import retrieve  # FAISS retriever (IMPORTANT)

# LLM powered RAG
from llm.llm_client import generate_response
from llm.prompt_builder import build_prompt

conversation_state = {
    "role": None,
    "skills": [],
}

# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------

def is_refinement(message: str) -> bool:
    keywords = ["also", "include", "add", "remove", "instead", "more", "only"]
    return any(k in message.lower() for k in keywords)


def is_comparison(message: str) -> bool:
    keywords = ["difference", "vs", "versus", "compare"]
    return any(k in message.lower() for k in keywords)


def is_refusal_query(message: str) -> bool:
    keywords = ["how should i hire", "write job description", "interview process"]
    return any(k in message.lower() for k in keywords)


def detect_prompt_injection(message: str) -> bool:
    keywords = ["ignore previous", "disregard", "amazon interview", "system prompt"]
    return any(k in message.lower() for k in keywords)


# -----------------------------
# MAIN FUNCTION
# -----------------------------

def handle_message(user_message):

    global conversation_state

    message = user_message.strip()

    # -------------------------
    # 1. PROMPT INJECTION BLOCK
    # -------------------------
    if detect_prompt_injection(message):
        return {
            "reply": "I can only recommend assessments from the SHL catalog.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------------------------
    # 2. REFUSAL BLOCK
    # -------------------------
    if is_refusal_query(message):
        return {
            "reply": "I'm only able to assist with selecting SHL assessments.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------------------------
    # 3. COMPARISON BLOCK
    # -------------------------
    if is_comparison(message):
        return {
            "reply": "Please provide the assessment names you want to compare.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------------------------
    # 4. REFINEMENT BLOCK
    # -------------------------
    if is_refinement(message) and conversation_state["role"] is not None:

        cleaned = message.lower().replace("add", "").replace("include", "").strip()
        conversation_state["skills"].append(cleaned)

        query = conversation_state["role"] + " " + " ".join(conversation_state["skills"])
        results = retrieve(query)

        return {
            "reply": "Updated recommendations based on your refinement:",
            "recommendations": results,
            "end_of_conversation": False
        }

    # -------------------------
    # 5. ASK ROLE
    # -------------------------
    if conversation_state["role"] is None:

        if message.lower() == "need assessment":
            return {
                "reply": "What role are you hiring for?",
                "recommendations": [],
                "end_of_conversation": False
            }

        conversation_state["role"] = message.strip()

        return {
            "reply": "What skills are important for this role?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------------------------
    # 6. ASK SKILLS
    # -------------------------
    if len(conversation_state["skills"]) == 0:

        conversation_state["skills"] = [
            s.strip().lower().replace("add", "").replace("include", "").strip()
            for s in message.split(",")
            if s.strip()
        ]

        return {
            "reply": "Got it. Searching best assessments for you...",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------------------------
    # 7. BUILD SEARCH QUERY
    # -------------------------
    query = conversation_state["role"] + " " + " ".join(conversation_state["skills"])

    # -------------------------
    # 8. FAISS RETRIEVAL
    # -------------------------
    results = retrieve(query)

    # -------------------------
    # 9. LLM PROMPT BUILD
    # -------------------------
    prompt = build_prompt(
        conversation_state["role"],
        conversation_state["skills"],
        results
    )

    llm_output = generate_response(prompt)

    return {
        "reply": llm_output,
        "recommendations": results,
        "end_of_conversation": True
    }


# -----------------------------
# RESET FUNCTION
# -----------------------------

def reset_state():
    global conversation_state
    conversation_state = {
        "role": None,
        "skills": [],
    }