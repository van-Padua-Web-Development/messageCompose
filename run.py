from _familySpin import create_app
import os

# Create Flask app using the factory
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)