import subprocess
import os
import webbrowser

running_process = None

def deploy_project(project_path="generated_project"):
    global running_process

    try:
        main_file = os.path.join(project_path, "main.py")

        if not os.path.exists(main_file):
            return {"status": "error", "message": "❌ main.py not found"}

        # Stop previous deployment if running
        if running_process:
            running_process.terminate()

        # Start new deployment
        running_process = subprocess.Popen(
            ["python", main_file],
            cwd=project_path
        )

        url = "http://localhost:5001"

        # Open browser automatically
        webbrowser.open(url)

        return {
            "status": "success",
            "message": "🚀 Deployment Successful",
            "url": url
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}