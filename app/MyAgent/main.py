from strands import Agent, tool
from strands.models import BedrockModel
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()


@tool
def word_count(text: str) -> int:
    """Count the number of words in a block of text.

    Args:
        text: The text to count words in.
    Returns:
        The number of whitespace-separated words.
    """
    return len(text.split())


# Amazon Nova Pro replaces the scaffold's Claude default.
model = BedrockModel(model_id="us.amazon.nova-pro-v1:0")

agent = Agent(
    model=model,
    tools=[word_count],
    system_prompt=(
        "You are a helpful assistant. You have a word_count tool. "
        "When the user asks how many words are in some text, use the "
        "word_count tool to answer precisely. For any other question, "
        "answer normally."
    ),
)


@app.entrypoint
def invoke(payload):
    """Handle an AgentCore Runtime invocation."""
    user_input = payload.get("prompt", "")
    response = agent(user_input)
    return response.message["content"][0]["text"]


if __name__ == "__main__":
    app.run()
