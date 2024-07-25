import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

class DocumentSuggester:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in .env file")
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate_api_documentation(self, code: str) -> str:
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0.7,
                system="You are a technical Product Manager skilled in explaining with documents. API design and documentation are your expertise.",
                messages=[
                    {"role": "user", "content": f"Write the API documentation for the following code:\n\n{code}"}
                ]
            )
            return message.content
        except Exception as e:
            return f"An error occurred: {str(e)}"
        
    def generate_code_from_api_documentation(self, api_documentation: str) -> str:
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0.7,
                system="You are a helpful assistant skilled in generating code from API documentation.",
                messages=[
                    {"role": "user", "content": f"Generate Java code for the following API documentation:\n\n{api_documentation}"}
                ]
            )
            return message.content
        except Exception as e:
            return f"An error occurred: {str(e)}"

def print_formatted_output(title, content):
    print(f"\n{'=' * 50}")
    print(f"{title}:")
    print(f"{'=' * 50}")
    if isinstance(content, str):
        print(content.strip())
    elif isinstance(content, list):
        for item in content:
            if hasattr(item, 'text'):
                print(item.text.strip())
            else:
                print(str(item).strip())
    else:
        print(str(content).strip())
    print(f"{'=' * 50}\n")

def main():
    sample_code = """
    def add(a: float, b: float) -> float:
        \"\"\"Add two numbers and return the result.\"\"\"
        return a + b

    def subtract(a: float, b: float) -> float:
        \"\"\"Subtract the second number from the first and return the result.\"\"\"
        return a - b
    """
    
    suggester = DocumentSuggester()
    
    print("Generating API Documentation...")
    documentation = suggester.generate_api_documentation(sample_code)
    print_formatted_output("Generated API Documentation", documentation)
    
    print("Generating code from API Documentation...")
    code = suggester.generate_code_from_api_documentation(documentation)
    print_formatted_output("Generated New Code", code)

if __name__ == "__main__":
    main()