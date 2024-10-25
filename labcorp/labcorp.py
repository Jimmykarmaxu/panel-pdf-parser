import pdfplumber
import re
import json

# Path to the PDF file
pdf_path = 'LabCorp 790020.pdf'

# Extract panel_id from the filename
panel_id = pdf_path.split('/')[-1].replace("LabCorp ", "").replace(".pdf", "")

def extract_data(pdf_path, panel_id):
    data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")

            current_drug_class = None
            metabolites = []

            for line in lines:
                line = line.strip()

                # Check if line contains the drug class in "TEST" column
                if re.match(r"^[A-Za-z\s]+(?:,\sUrine|\s\(Metab.\))", line):
                    # Save previous entry if it exists
                    if current_drug_class:
                        data.append({
                            "panel_id": panel_id,
                            "drug class": current_drug_class,
                            "Metabolite": metabolites
                        })
                    
                    # Extract drug class, ignoring additional descriptions
                    current_drug_class = re.split(r",|Negative|ng/mL|Cutoff", line)[0].strip()
                    metabolites = []

                # Check for metabolites line with "includes"
                elif "includes" in line.lower():
                    # Find capitalized words after "includes"
                    match = re.search(r"includes (.+)", line, re.IGNORECASE)
                    if match:
                        metabolites = [word for word in re.findall(r"\b[A-Z][a-z]*\b", match.group(1))]

            # Save the last drug class if exists
            if current_drug_class:
                data.append({
                    "panel_id": panel_id,
                    "drug class": current_drug_class,
                    "Metabolite": metabolites
                })

    return data

# Extract the data and convert it to JSON format
extracted_data = extract_data(pdf_path, panel_id)
json_output = json.dumps(extracted_data, indent=4)

# Print the final JSON result
print(json_output)