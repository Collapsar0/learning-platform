import platform

from app import create_app

if __name__ == "__main__":
    flask_app = create_app()
    if platform.system() == "Linux":
        flask_app.run(host="0.0.0.0", port=5555, debug=False)
    else:
        flask_app.run(host="0.0.0.0", port=5000, debug=True)
