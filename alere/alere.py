import pdfplumber
import json
import re

# Path to the PDF file
pdf_path = 'alere.pdf'


def extract_panel_tables(pdf_path):
    tables = []
    current_panel_id = None

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            # Find the Panel Description (Lab Test Code)
            panel_id_match = re.search(r'Panel Description of (?:Lab|Alere) Test Code (\d+)', text)
            if panel_id_match:
                current_panel_id = panel_id_match.group(1)
                # print(f"Panel ID found: {current_panel_id}")  # Debugging output

            # Extract the tables from the page
            raw_tables = page.extract_tables()
            for raw_table in raw_tables:
                if len(raw_table) > 0:
                    concatenated_row = []
                    for row in raw_table:  # Skip the header row
                        # If the row has fewer than 5 columns, treat it as an incomplete row
                        if len(row) < 5:
                            concatenated_row.extend(row)  # Combine with the next row
                        else:
                            if concatenated_row:
                                print(concatenated_row)
                                # Merge the incomplete concatenated_row with the current row
                                concatenated_row.extend(row)
                                row = concatenated_row  # Replace the current row with the concatenated one
                                concatenated_row = []  # Reset concatenated row for future use

                            # Now check if the row is valid (must have 5 columns after concatenation)
                            if len(row) == 5:
                                table_entry = {
                                    "panel_id": current_panel_id,
                                    "Drug Code": row[0].strip(),
                                    "Drug Class": row[1].strip().replace("\n", ""),
                                    "Metabolite": row[2].strip()[len("Including:\n- "):].replace("\n- ", ", ").replace("-\n", "").replace("\n", ""),
                                    "Screening Cut-Off": row[3].strip(),
                                    "Confirm Cut-Off": row[4].strip()
                                }
                                tables.append(table_entry)
                            else:
                                print(f"Incomplete or malformed row detected: {row}")  # Debugging output

    return tables

# Extract the tables and return them as a list of dictionaries
extracted_tables = extract_panel_tables(pdf_path)

# Convert the tables to JSON format
json_output = json.dumps(extracted_tables, indent=4)

# Display the final result
print(json_output)