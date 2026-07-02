def build_prompt(role, skills, retrieved_results):
    context = "\n".join([
        f"- {r['name']}: {r.get('description', '')}"
        for r in retrieved_results
    ])

    prompt = f"""
ROLE: {role}

SKILLS: {", ".join(skills)}

AVAILABLE SHL ASSESSMENTS:
{context}

TASK:
1. Recommend the best 5 assessments
2. Explain why each fits the role
3. Do NOT invent new assessments
4. Only use provided list
"""

    return prompt