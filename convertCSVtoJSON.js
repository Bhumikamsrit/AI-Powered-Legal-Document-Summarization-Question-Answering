// server/convertCSVtoJSON.js
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

// Path to input CSV file and output JSON file
const inputCSV = path.join(__dirname, '../data/legal_dataset.csv');
const outputJSON = path.join(__dirname, '../data/legal_dataset.json');

const cleanedData = [];

// Read and process the CSV file
fs.createReadStream(inputCSV)
    .pipe(csv())
    .on('data', (row) => {
        cleanedData.push({
            case_id: row.case_id,           // Keep the case_id
            case_outcome: row.case_outcome, // Keep the case_outcome
            case_title: row.case_title,     // Keep the case_title
            case_text: row.case_text        // Add the cleaned case_text
        });
    })
    .on('end', () => {
        console.log('CSV file successfully processed');

        // Save the cleaned data to JSON
        fs.writeFileSync(outputJSON, JSON.stringify(cleanedData, null, 2));
        console.log('Data saved to JSON:', outputJSON);
    });
