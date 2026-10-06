"""ACT Router — Analyze → Choose → Take Action → AI response pipeline."""

from app.act.analyzer import analyze
from app.act.chooser import choose, execute_tool
from app.services.ai_service import generate_response
from app.services.conversation_service import ConversationService


def process(
    user_input: str,
    conversation_history: list[dict] | None = None,
    learner_context: dict | None = None,
) -> dict:
    """Run the full ACT pipeline and return an AI-assisted response."""
    context_service = ConversationService(limit=8)
    for message in conversation_history or []:
        context_service.add(message)

    previous_context = context_service.build_context(user_input)
    analysis = analyze(user_input, previous_context, learner_context)
    intent = analysis["intent"]
    tool_name = choose(intent)

    try:
        tool_result = execute_tool(tool_name, user_input)
    except Exception as exc:
        tool_result = {
            "response": f"The local {tool_name} tool failed: {exc}",
            "type": "error",
            "data": None,
        }

    ai_result = generate_response(
        user_input,
        tool_result=tool_result,
        learner_context=learner_context,
        conversation_context=previous_context,
    )
    response = ai_result["response"]
    if not response:
        response = tool_result.get("response", "I could not determine a useful response.")

    return {
        "act": {
            "analyze": analysis,
            "choose": tool_name,
            "action": "completed",
        },
        "intent": intent,
        "response": response,
        "type": tool_result.get("type", "chat"),
        "source": ai_result["source"],
        "ai_unavailable": ai_result["ai_unavailable"],
        "tool": tool_result,
    }
