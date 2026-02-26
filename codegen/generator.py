import os

def generate_code(requirement, language="python"):
    
    output_dir = "build_output"
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, "main.py")

    code = """def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b

def main():
    print("Calculator Program Running...")
    print("10 + 5 =", add(10, 5))
    print("10 - 5 =", subtract(10, 5))
    print("10 * 5 =", multiply(10, 5))
    print("10 / 5 =", divide(10, 5))

if __name__ == "__main__":
    main()
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    return file_path