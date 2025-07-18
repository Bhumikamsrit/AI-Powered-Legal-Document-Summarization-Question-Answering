// server/convertCSVtoJSON.js
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

// Path to input CSV file and output JSON file
const inputCSV = path.join(__dirname, '../data/legal_dataset.csv');
const outputJSON = path.join(__dirname, '../data/legal_dataset.json');

// Optimized conversion with streaming and progress tracking
async function convertCSVtoJSON() {
    const cleanedData = [];
    let rowCount = 0;
    let errorCount = 0;

    return new Promise((resolve, reject) => {
        console.log('Starting CSV to JSON conversion...');
        console.log(`Input: ${inputCSV}`);
        console.log(`Output: ${outputJSON}`);

        // Check if input file exists
        if (!fs.existsSync(inputCSV)) {
            const error = `Input CSV file not found: ${inputCSV}`;
            console.error(error);
            reject(new Error(error));
            return;
        }

        const startTime = Date.now();

        fs.createReadStream(inputCSV)
            .pipe(csv())
            .on('data', (row) => {
                try {
                    // Validate required fields
                    if (!row.case_id || !row.case_text) {
                        console.warn(`Skipping row ${rowCount + 1}: Missing required fields`);
                        errorCount++;
                        return;
                    }

                    cleanedData.push({
                        case_id: row.case_id?.trim(),
                        case_outcome: row.case_outcome?.trim() || '',
                        case_title: row.case_title?.trim() || '',
                        case_text: row.case_text?.trim()
                    });

                    rowCount++;

                    // Progress reporting for large files
                    if (rowCount % 1000 === 0) {
                        console.log(`Processed ${rowCount} rows...`);
                    }
                } catch (err) {
                    console.warn(`Error processing row ${rowCount + 1}:`, err.message);
                    errorCount++;
                }
            })
            .on('end', () => {
                const endTime = Date.now();
                const duration = (endTime - startTime) / 1000;

                console.log(`CSV processing completed in ${duration}s`);
                console.log(`Total rows processed: ${rowCount}`);
                console.log(`Errors encountered: ${errorCount}`);
                console.log(`Valid records: ${cleanedData.length}`);

                if (cleanedData.length === 0) {
                    reject(new Error('No valid data found in CSV file'));
                    return;
                }

                try {
                    // Ensure output directory exists
                    const outputDir = path.dirname(outputJSON);
                    if (!fs.existsSync(outputDir)) {
                        fs.mkdirSync(outputDir, { recursive: true });
                    }

                    // Write JSON file with pretty formatting for readability
                    fs.writeFileSync(outputJSON, JSON.stringify(cleanedData, null, 2));
                    
                    console.log(`Data saved to JSON: ${outputJSON}`);
                    console.log(`File size: ${(fs.statSync(outputJSON).size / 1024 / 1024).toFixed(2)} MB`);
                    
                    resolve({
                        rowsProcessed: rowCount,
                        validRecords: cleanedData.length,
                        errors: errorCount,
                        outputFile: outputJSON,
                        duration: duration
                    });
                } catch (writeError) {
                    console.error('Error writing JSON file:', writeError);
                    reject(writeError);
                }
            })
            .on('error', (error) => {
                console.error('Error reading CSV file:', error);
                reject(error);
            });
    });
}

// Validate JSON output
function validateJSONOutput() {
    try {
        if (!fs.existsSync(outputJSON)) {
            throw new Error(`Output file not found: ${outputJSON}`);
        }

        const data = JSON.parse(fs.readFileSync(outputJSON, 'utf8'));
        
        if (!Array.isArray(data)) {
            throw new Error('JSON output is not an array');
        }

        const sampleRecord = data[0];
        if (!sampleRecord || !sampleRecord.case_id || !sampleRecord.case_text) {
            throw new Error('Invalid record structure in JSON output');
        }

        console.log(`✓ JSON validation passed: ${data.length} records`);
        return true;
    } catch (error) {
        console.error('✗ JSON validation failed:', error.message);
        return false;
    }
}

// Main execution
if (require.main === module) {
    convertCSVtoJSON()
        .then((result) => {
            console.log('\n✓ Conversion completed successfully:');
            console.log(JSON.stringify(result, null, 2));
            
            // Validate the output
            validateJSONOutput();
        })
        .catch((error) => {
            console.error('\n✗ Conversion failed:', error.message);
            process.exit(1);
        });
}

module.exports = { convertCSVtoJSON, validateJSONOutput };
