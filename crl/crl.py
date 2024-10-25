import pdfplumber
import json
import re

# Load the PDF with pdfplumber
pdf_path = 'crl.pdf'
results = []


with pdfplumber.open(pdf_path) as pdf:
    # Extract text from each page and process line-by-line
    text = ""
    for page in pdf.pages:
        lines = page.extract_text().splitlines()
        
        # Variable to hold the current screening test descriptor data
        current_screening_descriptor = None
        current_confirmation_descriptors = []
        
        # Iterate through lines to find Screening and Confirmation Descriptors
        for line in lines:
            # Check for the Panel ID once
            if "Panel ID:" in line:
                panel_id_match = re.search(r"Panel ID:\s*(\w+)", line)
                panel_id = panel_id_match.group(1) if panel_id_match else "Unknown"
            
            # Match Screening Test Descriptor
            screening_test_match = re.match(r"(\w+)\s+([A-Z/0-9\-]+\s+\(\d+/\d+\))\s+\d+\s*ng/mL", line)
            if screening_test_match:
                # If there is a previous screening test, save its results
                if current_screening_descriptor and current_confirmation_descriptors:
                    results.append({
                        "panel_id": panel_id,
                        "drug_class": current_screening_descriptor.strip(),
                        "Metabolite": current_confirmation_descriptors
                    })
                
                # Reset for the next screening test
                current_screening_descriptor = screening_test_match.group(2)
                current_confirmation_descriptors = []
            
            # Match Confirmation Test Descriptors (looking for LCMSMS descriptors)
            confirmation_test_match = re.search(r"([A-Z\s]+ LCMSMS\s*\(\d+\))", line)
            if confirmation_test_match:
                current_confirmation_descriptors.append(confirmation_test_match.group(1).strip())
        
        # Append the last set after finishing the loop
        if current_screening_descriptor and current_confirmation_descriptors:
            results.append({
                "panel_id": panel_id,
                "drug_class": current_screening_descriptor.strip(),
                "Metabolite": current_confirmation_descriptors
            })

# Convert the results to JSON format
json_output = json.dumps(results, indent=4)
print(json_output)