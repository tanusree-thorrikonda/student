from backend import create_app

# Instantiate the Flask application using our factory pattern
app = create_app()

if __name__ == '__main__':
    # Launch local development server in debug mode for active reload
    app.run(host='127.0.0.1', port=5000, debug=True)
