require("dotenv").config();
const natural = require("natural");
const { preprocessText } = require("./utils");
const { loadDataset } = require("./dataset");
const { OpenAI } = require("openai");

const TfIdf = natural.TfIdf;
const tfidf = new TfIdf();
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

let dataset = [];
let isInitialized = false;

// Optimized TF-IDF initialization with batching
async function initializeTFIDF() {
  if (isInitialized) {
    console.log("TF-IDF already initialized");
    return;
  }

  try {
    console.log("Starting TF-IDF initialization...");
    dataset = await loadDataset();
    
    // Process documents in batches to reduce memory pressure
    const batchSize = 100;
    let processed = 0;
    
    for (let i = 0; i < dataset.length; i += batchSize) {
      const batch = dataset.slice(i, i + batchSize);
      
      batch.forEach((doc) => {
        const cleanedText = preprocessText(doc.case_text);
        tfidf.addDocument(cleanedText);
        processed++;
      });
      
      // Log progress for large datasets
      if (processed % 1000 === 0) {
        console.log(`Processed ${processed}/${dataset.length} documents`);
      }
    }
    
    isInitialized = true;
    console.log(`TF-IDF model initialized with ${dataset.length} documents`);
  } catch (err) {
    console.error("Error initializing TF-IDF:", err);
    throw err;
  }
}

// Function to find the most relevant document based on TF-IDF
function findAnswerWithTFIDF(question) {
  if (!isInitialized || dataset.length === 0) {
    throw new Error("TF-IDF not initialized. Call initializeTFIDF first.");
  }

  const queryTokens = preprocessText(question).split(" ");
  const scores = [];

  dataset.forEach((doc, index) => {
    let score = 0;
    queryTokens.forEach((token) => {
      score += tfidf.tfidf(token, index);
    });
    scores.push({ index, score });
  });

  scores.sort((a, b) => b.score - a.score);
  const topDoc = dataset[scores[0]?.index];
  return topDoc ? topDoc.case_text : "No relevant document found.";
}

// Function to call NLP API (e.g., GPT-3 or GPT-4)
async function getAnswerWithNLPAPI(question) {
  try {
    const response = await openai.chat.completions.create({
      messages: [{ role: "user", content: question }],
      model: "gpt-3.5-turbo",
      max_tokens: 150,
    });
    return response.choices[0].message.content;
  } catch (error) {
    console.error("Error with OpenAI API:", error);
    return "Error processing the question.";
  }
}

// Reset function for testing
function resetTFIDF() {
  isInitialized = false;
  dataset = [];
  // Clear TF-IDF documents
  while (tfidf.documents.length > 0) {
    tfidf.documents.pop();
  }
}

// Export functions and initialize TF-IDF
module.exports = { 
  initializeTFIDF, 
  findAnswerWithTFIDF, 
  getAnswerWithNLPAPI,
  resetTFIDF,
  isInitialized: () => isInitialized
};
