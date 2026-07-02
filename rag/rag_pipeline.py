from rag.retriever import retrieve
from llm.llm_client import generate_response
from conversation.memory import ConversationMemory
from conversation.intent_handler import IntentHandler


intent = IntentHandler()
memory = ConversationMemory()

def build_context(results):
    """
    Convert retrieved SHL assessments into text for the LLM.
    """

    context = ""

    for i, assessment in enumerate(results, start=1):
        context += f"""
Assessment {i}

Name: {assessment['name']}

Description:
{assessment['description']}

Job Levels:
{assessment['job_levels']}

Languages:
{assessment['languages']}

Duration:
{assessment['duration']}

----------------------------------------
"""

    return context


def rag_chat(query: str):
    # Save user message
    memory.add_user_message(query)

    # Update conversation intent
    intent.update(query)

    # Ask clarification question if needed
    question = intent.next_question()

    if question:
        memory.add_assistant_message(question)
        return question

    # Build search query from extracted intent
    search_query = f"{intent.role} {intent.level}"
    #search_query = f"{intent.role} {intent.level} {intent.skills}"

    # Retrieve relevant assessments
    results = retrieve(search_query, top_k=10)

    # Build RAG context
    context = build_context(results)

    prompt = f"""
You are an SHL assessment recommendation assistant.

Conversation:
{memory.get_history()}

Relevant SHL Assessments:
{context}

User Request:
{query}

Recommend the best assessments with reasoning.
"""

    answer = generate_response(prompt)

    memory.add_assistant_message(answer)

    return answer