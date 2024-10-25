import pdfplumber
import re
import json

# Path to the PDF file
pdf_path = 'Quest 6633N.pdf'

# Parse panel_id from the filename by removing "Quest " prefix
panel_id = pdf_path.split('/')[-1].replace("Quest ", "").replace(".pdf", "")

def extract_data(pdf_path, panel_id):
    results = []
    current_drug_class = None
    metabolites = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text and split into lines
            text = page.extract_text()
            data_section = text.split("LEVEL TEST LEVEL METHOD", 1)[-1].split("Testing Lab")[0].strip()

            print(data_section);
            results = []
            current_drug = None
            for line in data_section.splitlines():
                line = line.strip()
                line = re.match(r"^[A-Za-z\s]+", line).group().strip()
                # Check if the line is an uppercase "drug_code" line
                if line.isupper():
                    # Save the previous drug object if it exists
                    if current_drug:
                        results.append(current_drug)

                    # Initialize a new drug object with drug_code
                    current_drug = {
                        "panel_id": panel_id,
                        "drug_code": line,
                        "Metabolite": []
                    }

                # If the line is capitalized (not fully uppercase), treat it as a metabolite
                elif current_drug and line[0].isupper() and not line.isupper():
                    # Extract only the leading words for the metabolite, discarding "ng/mL" and "MS"
                    metabolite_name = re.match(r"^[A-Za-z\s]+", line).group().strip()
                    current_drug["Metabolite"].append(metabolite_name)

    return results

# Extract results and convert to JSON format
extracted_data = extract_data(pdf_path, panel_id)
json_output = json.dumps(extracted_data, indent=4)

# Print the final JSON result
print(json_output)