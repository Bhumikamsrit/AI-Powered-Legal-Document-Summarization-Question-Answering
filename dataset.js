// server/dataset.js
const fs = require("fs");
const path = require("path");

// Load preprocessed legal dataset
const datasetPath = path.join(__dirname, "../data/legal_dataset.json");

function loadDataset() {
  return new Promise((resolve, reject) => {
    fs.readFile(datasetPath, "utf8", (err, data) => {
      if (err) {
        console.error("Error reading dataset:", err);
        reject(err);
        return;
      }

      try {
        const parsedData = JSON.parse(data);
        console.log("Dataset loaded successfully");
        resolve(parsedData);
      } catch (parseErr) {
        console.error("Error parsing dataset:", parseErr);
        reject(parseErr);
      }
    });
  });
}

module.exports = loadDataset;
