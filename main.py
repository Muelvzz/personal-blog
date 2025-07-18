from website import create_app

if __name__ == "__main__":
    main = create_app()
    main.run(debug=True)