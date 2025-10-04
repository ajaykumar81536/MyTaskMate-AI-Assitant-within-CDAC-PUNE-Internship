# tools/suggestion_agent.py
class SuggestionAgent:
    def provide_suggestion(self, user_prompt: str) -> str:
        prompt = user_prompt.lower()
        if "add task" in prompt and "due" not in prompt:
            return "Suggestion: Task added. You can reschedule it by its ID (e.g., 'reschedule task id 1 to 2025-12-25')."
        if "weather" in prompt:
            return "Suggestion: Would you like me to schedule an event based on this forecast?"
        if "show tasks" in prompt:
            return "Suggestion: You can mark tasks as complete by checking the box on the Tasks page."
        return ""