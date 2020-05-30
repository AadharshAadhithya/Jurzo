from Jurzo import create_app


jurzo = create_app()


if __name__ == '__main__':
    jurzo.run(debug=True, port=8097)
