import subprocess
import os

def build_project(project_path="generated_project"):
    try:
        main_file = os.path.join(project_path, "main.py")

        if not os.path.exists(main_file):
            return {"status": "error", "message": "main.py not found"}

        result = subprocess.run(
            ["python", "-m", "py_compile", main_file],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return {"status": "success", "message": "Build Successful ✅"}
        else:
            return {"status": "error", "message": result.stderr}

    except Exception as e:
        return {"status": "error", "message": str(e)}