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

    // Regular expression to find panel description, drug code, and metabolite data
    const panelRegex = /Panel Description of Alere Test Code (\d+)/g;

    // Updated regular expression to capture drug code, drug name, and metabolites
    const drugPattern =
      /([A-Z]+)\s+([\w/\- ]+)\s+Including:\s+(- [\w, \-/]+)+/g;

    let match;
    const results = [];

    // Collect all matches for panel descriptions
    const panelMatches = [];
    while ((match = panelRegex.exec(fullText)) !== null) {
      panelMatches.push({ panelCode: match[1], index: match.index });
    }
      
    console.log(panelMatches);

    // Loop over each panel description and extract the data between them
    for (let i = 0; i < panelMatches.length; i++) {
      const panelCode = panelMatches[i].panelCode;
      const panelTextStart = panelMatches[i].index;
      const panelTextEnd =
        i + 1 < panelMatches.length
          ? panelMatches[i + 1].index
          : fullText.length;

      // Extract the text between this panel and the next
      const panelText = fullText.slice(panelTextStart, panelTextEnd);

      let drugMatch;
      // Find drug codes and metabolites in the panel text
      while ((drugMatch = drugPattern.exec(panelText)) !== null) {
        const drugCode = drugMatch[1].trim();
        const drugName = drugMatch[2].trim();

        // Extract metabolites by splitting on hyphen and removing empty spaces
        const metabolitesList = drugMatch[0]
          .match(/- [\w, \-/]+/g)
          .map((m) => m.replace('- ', '').trim());

        results.push({
          panel: panelCode,
          drug_code: drugCode,
          drug_name: drugName,
          metabolites: metabolitesList,
        });
      }

      // Log if no matches were found
      if (results.length === 0) {
        console.log(`No drug matches found for Panel ${panelCode}`);
      }
    }

    return results;
  } catch (error) {
    console.error('Error reading or parsing the PDF file:', error);
  }
}

// Example usage:
// Use path.resolve to create an absolute file path to the PDF
const pdfPath = path.resolve('path_to_your_pdf_file.pdf'); // Update with your actual file path
extractMetaboliteDataFromPDF(pdfPath)
  .then((metaboliteData) => {
    console.log(JSON.stringify(metaboliteData, null, 2));
  })
  .catch((error) => {
    console.error('Error parsing PDF:', error);
  });