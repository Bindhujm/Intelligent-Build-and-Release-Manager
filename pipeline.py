from codegen.generator import generate_code
from builder.builder import build_project

def run_pipeline():
    print("Pipeline Started")

    # Step 1: Generate Code
    print("Generating Code...")
    generated_file = generate_code("Simple calculator", "python")

    if not generated_file:
        print("Code Generation Failed")
        return

    print("Code Generated Successfully")

    # Step 2: Build Project
    print("Building Project...")
    success = build_project()

    if success:
        print("Build Successful")
    else:
        print("Build Failed")

if __name__ == "__main__":
    run_pipeline()



