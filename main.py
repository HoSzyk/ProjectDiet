from dietapp import app

if __name__ == '__main__':
    # Create database tables
    # Application server run
    app.run(debug=True, use_reloader=False)
