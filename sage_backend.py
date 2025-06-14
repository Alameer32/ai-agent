import requests
import json
import os

# === Config ===
USER_PROFILE_FILE = "user_profile.json"
MEMORY_FILE = "memory.json"
MODEL_NAME = "mistral"  # or "llama3" etc.
OLLAMA_URL = "http://localhost:11434/api/generate"
DEBUG = False  # Toggle to print full prompt for inspection

# === User Profile ===
def load_user_profile(path=USER_PROFILE_FILE):
    with open(path, "r") as file:
        return json.load(file)

def save_user_profile(profile, path=USER_PROFILE_FILE):
    with open(path, "w") as file:
        json.dump(profile, file, indent=2)

# === Memory ===
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as file:
        return json.load(file)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=2)

def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

def recall():
    memory = load_memory()
    if not memory:
        return "I currently have no memories about you."
    return "\n".join(f"- {v}" for v in memory.values())

# === AI Agent Logic ===
user_profile = load_user_profile()

system_prompt = (
    f"You are SAGE, a helpful and calm AI assistant designed to help {user_profile['name']}, "
    f"a {user_profile['profession']} from {user_profile['location']}. "
    f"Speak like a friendly human in short replies — no more than 2 to 3 sentences. "
    f"Don't introduce yourself every time. Keep it natural, relaxed, and supportive, like chatting with a friend."
)
def ask_ollama(prompt, conversation):
    memory_text = recall()
    history = f"{system_prompt}\n\nKnown facts:\n{memory_text}\n\n"

    for user_msg, agent_msg in conversation:
        if isinstance(user_msg, str) and isinstance(agent_msg, str):
            history += f"User: {user_msg.strip()}\nAI: {agent_msg.strip()}\n"

    history += f"User: {prompt.strip()}\nAI:"

    if DEBUG:
        print("\n--- DEBUG: Full prompt sent to Ollama ---")
        print(history)
        print("--- END PROMPT ---\n")

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": history,
                "stream": False
            },
            timeout=60
        )
        return response.json().get("response", "Sorry, no response from the model.")
    except Exception as e:
        return f"Error talking to Ollama: {str(e)}"

# === Main Loop ===
if __name__ == "__main__":
    print(f"👋 Hello {user_profile['name']}, SAGE is ready to assist you.")
    print("💡 Type 'exit' to quit, or 'remember that ...' to store new info.\n")

    conversation = []

    while True:
        user_input = input("🧑 You: ").strip()
        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # Save memory
        if user_input.lower().startswith("remember that "):
            fact = user_input[len("remember that "):].strip()
            if fact:
                key = f"fact_{len(load_memory()) + 1}"
                remember(key, fact)
                print(f"🤖 SAGE: Got it. I'll remember that: '{fact}'")
            else:
                print("🤖 SAGE: Please specify what you'd like me to remember.")
            continue

        # Recall memory
        if user_input.lower() in [
            "what do you remember",
            "recall memory",
            "what do you know about me"
        ]:
            print(f"🤖 SAGE: Here’s what I remember about you:\n{recall()}")
            continue

        # AI response
        agent_reply = ask_ollama(user_input, conversation)
        conversation.append((user_input, agent_reply))
        print(f"🤖 SAGE: {agent_reply}")
