// server/dataset.js
const fs = require("fs").promises;
const path = require("path");

// Load preprocessed legal dataset
const datasetPath = path.join(__dirname, "../data/legal_dataset.json");

// Cache for loaded dataset
let cachedDataset = null;
let lastModified = null;

async function loadDataset() {
  try {
    // Check if file has been modified since last load
    const stats = await fs.stat(datasetPath);
    const currentModified = stats.mtime.getTime();
    
    // Return cached dataset if file hasn't changed
    if (cachedDataset && lastModified === currentModified) {
      console.log("Using cached dataset");
      return cachedDataset;
    }

    console.log("Loading dataset from file...");
    const data = await fs.readFile(datasetPath, "utf8");
    const parsedData = JSON.parse(data);
    
    // Update cache
    cachedDataset = parsedData;
    lastModified = currentModified;
    
    console.log(`Dataset loaded successfully: ${parsedData.length} documents`);
    return parsedData;
  } catch (err) {
    console.error("Error loading dataset:", err);
    throw err;
  }
}

// Clear cache function for testing/development
function clearCache() {
  cachedDataset = null;
  lastModified = null;
}

module.exports = { loadDataset, clearCache };
