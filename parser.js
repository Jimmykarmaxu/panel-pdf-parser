const fs = require('fs');
const pdf = require('pdf-parse');
const path = require('path'); // Import path module to handle file paths

async function extractMetaboliteDataFromPDF(pdfPath) {
  try {
    // Ensure the file exists and read it
    const dataBuffer = fs.readFileSync(pdfPath);

    // Parse the PDF using pdf-parse
    const data = await pdf(dataBuffer);
    let fullText = data.text;

    // Clean up the text: remove excessive newlines, multiple spaces, and other irregularities
    fullText = fullText.replace(/\s+/g, ' ').trim();

    // Regular expression to match the drug code, drug name, and metabolites
    const drugPattern =
      /([A-Z]+)\s+([\w/\- ]+)\s+Including:\s+(- [\w, \-/]+(?:\s*- [\w, \-/]+)*)/g;

    let match;
    const results = [];

    // Loop over matches for the drug pattern
    while ((match = drugPattern.exec(fullText)) !== null) {
      const drugCode = match[1];
      const drugName = match[2].trim();

      // Extract metabolites, remove hyphen and clean up
      const metabolites = match[3]
        .split('-')
        .map((m) => m.trim())
        .filter((m) => m.length > 0);

      results.push({
        drug_code: drugCode,
        drug_name: drugName,
        metabolites: metabolites,
      });
    }

    return results;
  } catch (error) {
    console.error('Error reading or parsing the PDF file:', error);
  }
}

// Example usage:
const pdfPath = 'path_to_your_pdf_file.pdf'; // Replace with the actual path to your PDF file
extractMetaboliteDataFromPDF(pdfPath)
  .then((metaboliteData) => {
    console.log(JSON.stringify(metaboliteData, null, 2));
  })
  .catch((error) => {
    console.error('Error parsing PDF:', error);
  });