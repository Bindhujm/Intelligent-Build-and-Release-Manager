from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import subprocess
import re
import os
from flask import Flask
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")

app = Flask(__name__)

client = Groq(api_key=api_key)

app = Flask(__name__)
CORS(app)

# 🔑 PUT YOUR GROQ API KEY HERE
client = Groq(api_key=api_key)

# Ensure build folder exists
os.makedirs("build_output", exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


# ======================================
# GENERATE AI CODE
# ======================================

@app.route("/generate", methods=["POST"])
def generate():
    try:
        user_input = request.json.get("requirement")

        if not user_input:
            return jsonify({"error": "No requirement provided"}), 400

        prompt = f"""
        Generate a COMPLETE executable Python program for:

        {user_input}

        STRICT RULES:
- Must be syntactically correct
- Every function must have a body
- Use pass if needed
- No explanation text
- No markdown
- Return only Python code
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response.choices[0].message.content

        import re

        # Remove markdown
        cleaned = re.sub(r"```python", "", raw_output)
        cleaned = re.sub(r"```", "", cleaned)
        cleaned = cleaned.strip()

        # Add pass to empty function definitions
        cleaned = re.sub(
            r"(def .*?:\n)(\s*\n)",
            r"\1    pass\n",
            cleaned
        )

        # Add pass to empty if statements
        cleaned = re.sub(
            r"(if .*?:\n)(\s*\n)",
            r"\1    pass\n",
            cleaned
        )

        with open("build_output/main.py", "w", encoding="utf-8") as f:
            f.write(cleaned)

        return jsonify({
            "status": "success",
            "code": cleaned
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
# ======================================
# BUILD (CHECK SYNTAX ONLY)
# ======================================
@app.route("/build", methods=["POST"])
def build():
    import py_compile
    import traceback

    file_path = "build_output/main.py"

    try:
        # First compilation attempt
        py_compile.compile(file_path, doraise=True)

        return jsonify({
            "status": "success",
            "message": "Build Successful ✅"
        })

    except Exception as first_error:
        # Auto-repair common indentation issues
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            fixed_lines = []

            for i in range(len(lines)):
                line = lines[i]

                # If function has no body, add pass
                if line.strip().startswith("def ") and (
                    i + 1 >= len(lines) or lines[i + 1].strip() == ""
                ):
                    fixed_lines.append(line)
                    fixed_lines.append("    pass\n")
                else:
                    fixed_lines.append(line)

            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(fixed_lines)

            # Retry compilation
            py_compile.compile(file_path, doraise=True)

            return jsonify({
                "status": "success",
                "message": "Build Successful After Auto-Fix ✅"
            })

        except Exception:
            return jsonify({
                "status": "failure",
                "message": traceback.format_exc()
            })

# ======================================
# DEPLOY (RUN PROGRAM)
# ======================================
@app.route("/deploy", methods=["POST"])
def deploy():
    try:
        result = subprocess.run(
            ["python", "build_output/main.py"],
            capture_output=True,
            text=True,
            timeout=15
        )

        if result.returncode == 0:
            return jsonify({
                "status": "success",
                "output": result.stdout
            })
        else:
            return jsonify({
                "status": "failure",
                "output": result.stderr
            })

    except Exception as e:
        return jsonify({
            "status": "failure",
            "output": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)