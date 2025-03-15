# AI-Powered-Legal-Document-Summarization-Question-Answering

We have obtained the dataset from Kaggle using the following link: https://www.kaggle.com/datasets/amohankumar/legal-text-classification-dataset?resource=download

The dataset contains a total of 25152 legal cases in the form of text documents. Each document has been annotated with catchphrases, citations sentences, citation catchphrases, and citation classes. Citation classes indicate the type of treatment given to the cases cited by the present case. The Legal Citation Text Classification dataset is provided in CSV format. The dataset has four columns, namely Case ID, Case Outcome, Case Title, and Case Text. The Case ID column contains a unique identifier for each legal case, the Case Outcome column indicates the outcome of the case, the Case Title column contains the title of the legal case, and the Case Text column contains the text of the legal case.

Install Dependencies:

Ensure you have Node.js installed. Then, execute:

npm install
Dataset Preparation
Obtain Dataset:

Acquire a legal document dataset suitable for summarization and question-answering tasks. Publicly available datasets can be found in research publications or repositories.

Place Dataset:

Save the dataset files in the data/ directory. Ensure the dataset is in a compatible format (e.g., JSON, CSV) for processing. If your dataset is in CSV format, convert it to JSON by running the following command:

npm run convert-csv-to-json
Usage
Start the Application:

npm start
This command initializes the API endpoints and serves a simple UI at http://localhost:3000. The UI includes a text input field for entering questions, a submit button to send the question, and a result section displaying the response.

Access Functionality:

Utilize tools like Postman or curl to interact with the API endpoints for summarization and clause extraction.

API Endpoints
The application offers the following endpoints:

Extractive Summarization:

Endpoint: /summarize

Method: POST

Description: Generates a concise summary by extracting key sentences from the legal document.

Request Body:

{
  "document": "Full text of the legal document."
}
Response:

{
  "summary": "Extracted summary of the document."
}
Abstractive Summarization:

Endpoint: /abstractive_summarize

Method: POST

Description: Produces a summary by interpreting and paraphrasing the content of the legal document.

Request Body:

{
  "document": "Full text of the legal document."
}
Response:

{
  "summary": "Abstractive summary of the document."
}
Clause Extraction:

Endpoint: /extract_entities

Method: POST

Description: Identifies and extracts specific clauses or entities from the legal document.

Request Body:

{
  "document": "Full text of the legal document."
}
Response:

{
  "clauses": [
    "Extracted clause 1.",
    "Extracted clause 2.",
    ...
  ]
}
Project Structure
The repository is organized as follows:

NLP---Legal-document-summarization-and-question-answering/
├── data/                        # Directory for datasets
│   ├── legal_dataset.csv
│   └── legal_dataset.json                      
├── public/                      # Directory for UI
│   └── index.html                      
├── script/                      # Directory for scripts
│   └── convertCSVtoSJON.js                       
├── server/                      # Directory for server-related files
│   ├── clause_extraction.js             
│   ├── dataset.js             
│   ├── nlp.js              
│   ├── preprocess.js              
│   ├── routes.js                
│   ├── server.js                
│   ├── summarization.js
│   └── utils.js                 
├── package.json                 # Node.js dependencies and scripts
├── .gitignore                   # Git ignore file
└── README.md                    # Project documentation
Code Overview
server.js
This is the main entry point of the application. It sets up the Express server, configures middleware, and defines the primary routes.

Imports:

express: Framework for building web applications.
body-parser: Middleware for parsing incoming request bodies.
path: Contains utilities for working with file and directory paths
Route handlers from the routes directory.
Middleware:

body-parser.json(): Parses incoming JSON requests.
body-parser.urlencoded({ extended: true }): Parses URL-encoded data.
Routes:

/summarize: Handles extractive summarization requests.
/abstractive_summarize: Handles abstractive summarization requests.
/extract_entities: Handles clause extraction requests.
Server Initialization:

The server listens on the port specified in config.js.
server/
The server directory contains route handler modules for different API endpoints, core logic, and utilities for performing NLP tasks.

server/summarization.js
Handles POST requests to /summarize.

Key Steps:
Extracts the document text from the request body:
const { document } = req.body;
Passes the text to a service function (e.g., summarizeText) from the services directory.
Returns the extracted summary in the response:
res.json({ summary });
Handles POST requests to /abstractive_summarize.

Key Steps:
Extracts the document text from the request body:
const { document } = req.body;
Passes the text to the abstractive summarization service function (e.g., generateAbstractiveSummary).
Returns the abstractive summary in the response:
res.json({ summary });
server/clause_extraction.js
Handles POST requests to /extract_entities.
Key Steps:
Extracts the document from the request body:
const { document } = req.body;
Calls the clause or entity extraction service function (e.g., extractClauses).
Returns the extracted clauses or entities:
res.json({ clauses });
server/summarization.js
summarizeText Function:

Implements extractive summarization using techniques like:
Sentence tokenization to split the document into sentences.
Sentence scoring based on frequency, importance, or position.
Selection of top-scoring sentences to form the summary.
Example code snippet:
function summarizeText(document) {
  const sentences = tokenize(document);
  const scoredSentences = scoreSentences(sentences);
  return selectTopSentences(scoredSentences);
}
generateAbstractiveSummary Function:

Uses a pre-trained NLP model (e.g., Hugging Face's Transformers library) for generating a paraphrased summary:
const model = loadModel('abstractive-summarizer');
const summary = model.generate(document);
return summary;
server/clause_extraction.js
extractClauses Function:
Applies Named Entity Recognition (NER) or regex-based matching to identify legal clauses or key entities.
Example:
const clauses = nerModel.findEntities(document, ['Clause', 'Section']);
return clauses;
Example Utility Functions
tokenize:

Splits text into sentences or words for processing:
function tokenize(text) {
  return text.split(/\.|\?|\!/).filter(Boolean);
}
scoreSentences:

Assign scores to sentences based on term frequency or other metrics:
function scoreSentences(sentences) {
  return sentences.map(sentence => ({
    sentence,
    score: calculateScore(sentence),
  }));
}
Configuration
config.js
Contains project-wide settings, such as:
Default server port:
const PORT = process.env.PORT || 3000;
API key or model configurations:
const MODEL_CONFIG = {
  summarizer: 'path/to/model',
  qaModel: 'path/to/qa-model',
};
Dependencies
Node.js: Backend framework for building scalable server-side applications.

Natural Language Processing Libraries
@xenova/transformers: Implements Hugging Face Transformers for advanced NLP tasks.
compromise: A lightweight library for basic text processing.
natural: A comprehensive NLP library for tokenization, stemming, classification, and more.
node-summarizer: Used for summarizing lengthy text documents.
Data Handling
csv-parser: Parses CSV files into JavaScript objects for easier processing.
Backend Framework and Middleware
express: A minimal and flexible Node.js web application framework for building APIs.
body-parser: Middleware for parsing incoming request bodies, including JSON data.
AI API Integration
openai: Provides tools to integrate and interact with OpenAI’s API for advanced question-answering functionality.
Environment Configuration
dotenv: Enables secure management of environment variables by loading them from a .env file.
Utility Libraries
uri-js: Assists in manipulating and working with Uniform Resource Identifiers (URIs).
offscreen-canvas: Supports offscreen rendering for graphical operations.
Machine Learning Framework
onnxruntime-node: Executes ONNX models efficiently in a Node.js environment.
Development Tools
nodemon: Automatically restarts the server during development whenever file changes are detected.
