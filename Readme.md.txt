# Phone Number OSINT Tool

## Overview

This project is an Open Source Intelligence (OSINT) tool for gathering information about phone numbers using the TruecallerPy library. The tool features a graphical user interface (GUI) built with Tkinter, allowing users to search for phone numbers and retrieve associated information such as names, addresses, and more.

## Features

- Search for phone numbers to gather detailed information
- Retrieve name, address, and other associated details of phone numbers
- User-friendly graphical interface using Tkinter
- Supports batch processing of multiple phone numbers

## Prerequisites

- Python 3.7 or higher
- TruecallerPy library
- Truecaller account for accessing the API

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/phone-number-osint.git
    cd phone-number-osint
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Install TruecallerPy:

    ```sh
    pip install truecallerpy
    ```

## Usage

1. Obtain your Truecaller credentials (username and password).

2. Configure your credentials in a `config.json` file in the root of the project:

    ```json
    {
      "username": "your_truecaller_username",
      "password": "your_truecaller_password"
    }
    ```

3. Run the Tkinter-based GUI:

    ```sh
    python gui.py
    ```

## Example

To start the GUI:

```sh
python gui.py
