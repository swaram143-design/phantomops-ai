from langchain_ollama import OllamaLLM

print("Starting Jarvis...")

llm = OllamaLLM(model="phi3")

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Jarvis shutting down...")
        break

    try:
        response = llm.invoke(question)
        print("\nJarvis:", response)

    except Exception as e:
        print("Error:", e)