# UGC Chatbot for University Admission Enquiries

This repository contains the code and resources for a chatbot built using Rasa framework to handle UGC-related enquiries and university admission-related queries in Sri Lanka.

## About

The UGC Chatbot is designed to provide assistance to students seeking information about universities, admission requirements, programs offered, policies, scholarships, and other relevant details. The chatbot is built using Rasa, an open-source conversational AI framework.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/ugc-chatbot.git
Change into the project directory:

shell
Copy code
cd ugc-chatbot
Create a virtual environment:

shell
Copy code
python -m venv env
Activate the virtual environment:

On Linux/macOS:

shell
Copy code
source env/bin/activate
On Windows:

shell
Copy code
env\Scripts\activate
Install the required dependencies:

shell
Copy code
pip install -r requirements.txt
Usage
To train and run the UGC Chatbot, follow these steps:

Train the Rasa model:

shell
Copy code
rasa train
Start the Rasa action server:

shell
Copy code
rasa run actions
Start the Rasa chatbot server:

shell
Copy code
rasa run --enable-api
Interact with the chatbot using the provided user interface or by sending API requests.

Customization
You can customize the chatbot's responses, intents, stories, and actions by modifying the relevant files in the project directory. The training data can be found in the data directory, and the response templates can be modified in the domain.yml file
