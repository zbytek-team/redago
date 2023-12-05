# Redago

This repository houses components for the Redago application, an AI-driven tool for language correction in Polish texts.

## Structure

The repository is organized into the following components:

### `redago_backend`

The `redago_backend` directory contains the backend application built using LiteStar, responsible for handling user requests and utilizing `redago_core` for text corrections.

### `redago_core`

The `redago_core` directory houses the core functionality responsible for text correction, language processing, and AI models.

### `redago_data_loader`

The `redago_data_loader` directory includes functionality for fetching books from the `wolnelektury.pl` API and preparing them for processing by the AI model.

### `redago_model`

The `redago_model` directory encompasses the model training functionality, utilizing advanced AI models like BERT for text correction and language enhancement.

### `redago_tests`

The `redago_tests` directory contains various tests, including efficiency and accuracy tests for the correction process.

### `redago_web_app`

The `redago_web_app` directory hosts the frontend application, developed using React, enabling users to send text correction requests.

## Getting Started

Install dependencies by running `pip install -r requirements.txt`.

### Running model tools

1. **Data Loader Setup**:
   - Navigate to the `redago_data_loader` directory.
   - Fetch books by running `python3 api_loader.py`.

2. **Comma Model Setup**:
   - Navigate to the `redago_model/comma-model` directory.
   - Train model with `python3 data.py <input_dir> [output_dir]`.
   - Save model on `https://huggingface.co/`.

3. **Efficiency Tester Setup**:
   - Navigate to the `redago_tests/efficiency_tester` directory.
   - Test efficiency by running `python3 main.py`.

**Setting Environment Variables**:
   - Create a `.env` file in the root directory of the project.
   - Define the following variables inside the `.env` file:
     ```
     HUGGINGFACE_TOKEN=<token>
     MODEL_NAME=<model-name>
     PYTHONPATH=<project-path>
     ```
   - Load these variables in your terminal:
     ```
     set -a
     source .env
     set +a
     ```
   - Ensure these variables are properly set before running any scripts or components within the Redago project.

### Running app locally

1. **Backend Setup**:
   - Navigate to the `redago_backend` directory.
   - Start the backend server with `python3 run.py`.

2. **Frontend Setup**:
   - Go to the `redago_web_app` directory.
   - Install dependencies using `npm install`.
   - Launch the frontend app with `npm run dev`.

3. **Usage**:
   - Access the frontend at `http://localhost:5173`.
   - Send text correction requests via the frontend, which will be handled by the backend utilizing the `redago_core` functionalities.

## Dockerization

Both the backend and frontend applications can be Dockerized for easy deployment. Refer to individual directories for Dockerfile configurations.

To Dockerize the backend:
1. Use `docker-compose up -d` to build and start all services defined in the `docker-compose.yml` file.
2. Access the application at appropriate ports mapped in the `docker-compose.yml` file.

## Contributing

Feel free to contribute to Redago by opening issues or submitting pull requests. We welcome any improvements or bug fixes!

## License

This project is licensed under the [MIT License](LICENSE).