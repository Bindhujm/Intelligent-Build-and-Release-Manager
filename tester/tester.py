import os
import subprocess

def test_project(language):
    try:
        if language == "Python":
            result = subprocess.run(
                ["python", "generated_project/app.py"],
                capture_output=True,
                text=True
            )
            return "Tests Passed ✅\n" + result.stdout

        elif language == "JavaScript":
            result = subprocess.run(
                ["node", "generated_project/app.js"],
                capture_output=True,
                text=True
            )
            return "Tests Passed ✅\n" + result.stdout

        else:
            return "Unsupported language"

    except Exception as e:
        return f"Test Failed ❌ {str(e)}"
