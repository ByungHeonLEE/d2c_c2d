import os
import anthropic
from dotenv import load_dotenv
from datetime import datetime

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

def create_directory_structure():
    base_dir = 'results'
    code_dir = os.path.join(base_dir, 'code')
    docu_dir = os.path.join(base_dir, 'docu')
    
    os.makedirs(code_dir, exist_ok=True)
    os.makedirs(docu_dir, exist_ok=True)
    
    return code_dir, docu_dir

def save_to_file(content, directory, prefix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.txt"
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'w') as file:
        if isinstance(content, list):
            for item in content:
                if hasattr(item, 'text'):
                    file.write(item.text + '\n')
                else:
                    file.write(str(item) + '\n')
        elif isinstance(content, str):
            file.write(content)
        else:
            file.write(str(content))
    
    print(f"Content saved to {filepath}")

def main():
    sample_code = """
    def add(a: float, b: float) -> float:
        \"\"\"Add two numbers and return the result.\"\"\"
        return a + b

    def subtract(a: float, b: float) -> float:
        \"\"\"Subtract the second number from the first and return the result.\"\"\"
        return a - b
    """
    
    code_dir, docu_dir = create_directory_structure()
    suggester = DocumentSuggester()
    
    print("Generating API Documentation...")
    documentation = suggester.generate_api_documentation(sample_code)
    print_formatted_output("Generated API Documentation", documentation)
    save_to_file(documentation, docu_dir, "api_documentation")
    
    print("Generating code from API Documentation...")
    code = suggester.generate_code_from_api_documentation(documentation)
    print_formatted_output("Generated New Code", code)
    save_to_file(code, code_dir, "generated_code")

if __name__ == "__main__":
    main()