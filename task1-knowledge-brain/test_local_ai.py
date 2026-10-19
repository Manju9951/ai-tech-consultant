
import ollama

response = ollama.chat(
    model="llama3.2:1b",
    messages=[
        {
            "role": "user",
            "content": "Explain AI Tech Consultant in simple English."
        }
    ]
)

print(response["message"]["content"])
