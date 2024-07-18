# MCQ Generator with Generative AI

This project is a Multiple Choice Question (MCQ) generator using Generative AI. It utilizes the OpenAI API to generate quizzes and evaluate them.

## Directory Structure


- **.env**: Contains environment variables.
- **.vscode**: Contains VSCode specific settings.
- **logs**: Directory to store log files.
- **__pycache__**: Directory for Python cache files.
- **.gitignore**: Git ignore file.
- **logger.py**: Module for logging.
- **main.py**: Main script for generating and evaluating MCQs.
- **quiz_output.txt**: Output file for quiz generation.
- **Response.json**: Sample response JSON.
- **secretkey.py**: File containing secret keys.
- **streamlitapp.py**: Streamlit application file.
- **test.py**: Test script.
- **The Bombay Stock Exchange (BSE) is .txt**: Sample text file.
- **utils.py**: Utility functions.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/mcq-generator.git
    cd mcq-generator
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv .env
    source .env/bin/activate  # On Windows use `.env\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the OpenAI API key:
    - Add your OpenAI API key to the `secretkey.py` file.

## Usage

1. **Generating MCQs**:
    - Run the `main.py` script to generate MCQs based on a given text.
    ```sh
    python main.py
    ```

2. **Streamlit Application**:
    - Run the Streamlit app to interact with the MCQ generator.
    ```sh
    streamlit run streamlitapp.py
    ```

## Logging

- Logs are stored in the `logs` directory. The `logger.py` module is used for logging various activities within the application.

## Testing

- Use the `test.py` script for running tests.
    ```sh
    python test.py
    ```

## Sample Files

- `The Bombay Stock Exchange (BSE) is .txt`: Sample text file for generating MCQs.
- `Response.json`: Sample response JSON for reference.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Thanks to OpenAI for providing the API for generating quizzes.
