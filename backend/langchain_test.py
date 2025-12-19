from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="llama3.2:3b"
)

response = llm.invoke("Say hello in one short sentence.")
print(response)
