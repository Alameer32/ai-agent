import requests
import json
import os

# Files
USER_PROFILE_FILE = "user_profile.json"
MEMORY_FILE = "memory.json"

# Load user profile from JSON
def load_user_profile(path=USER_PROFILE_FILE):
    with open(path, "r") as file:
        return json.load(file)

# Save updates to user profile (optional usage)
def save_user_profile(profile, path=USER_PROFILE_FILE):
    with open(path, "w") as file:
        json.dump(profile, file, indent=2)

# Memory helpers
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

def recall():
    memory = load_memory()
    if not memory:
        return "I currently have no memories about you."
    return "\n".join(f"- {v}" for v in memory.values())

# Load user profile once
user_profile = load_user_profile()

# Build system prompt using user profile details
system_prompt = (
    f"You are SAGE, a wise and articulate AI assistant designed to help {user_profile['name']}, "
    f"a {user_profile['profession']} located at {user_profile['location']}. "
    f"He is interested in {', '.join(user_profile['interests'])}, and currently focused on: "
    f"{'; '.join(user_profile['goals'])}. Use a {user_profile['personality_preferences']['tone']} tone, "
    f"be {user_profile['personality_preferences']['assistant_behavior']}, and keep responses like a hlepful friend and natural texting."
)

def ask_ollama(prompt, conversation):
    memory_text = recall()
    # Build conversation history + memory + system prompt
    history = f"{system_prompt}\n\nMemory of you:\n{memory_text}\n\n"
    for user_msg, agent_msg in conversation:
        history += f"User: {user_msg}\nAI: {agent_msg}\n"
    history += f"User: {prompt}\nAI:"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": history,
            "stream": False
        }
    )
    response_json = response.json()
    return response_json.get("response", "Sorry, no response from the model.")

if __name__ == "__main__":
    print(f"Hello {user_profile['name']}, SAGE is ready to assist you.")
    print("Type 'exit' to quit.\n")

    conversation = []

    while True:
        user_input = input("💬 You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # Memory add command
        if user_input.lower().startswith("remember that "):
            fact = user_input[len("remember that "):].strip()
            key = f"fact_{len(load_memory()) + 1}"
            remember(key, fact)
            print(f"🤖 SAGE: Got it, I'll remember that: '{fact}'")
            continue

        # Optionally, add a command to recall all memories
        if user_input.lower() in ["what do you remember", "recall memory", "what do you know about me"]:
            mem_text = recall()
            print(f"🤖 SAGE: Here is what I remember about you:\n{mem_text}")
            continue

        # Otherwise, send to Ollama
        agent_reply = ask_ollama(user_input, conversation)
        conversation.append((user_input, agent_reply))
        print(f"🤖 SAGE: {agent_reply}")
