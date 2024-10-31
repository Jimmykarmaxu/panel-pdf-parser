# Mapping data
row_data = {
    "6-Monoacetylmorphine": "6-monoacetylmorphine",
    "Amphetamine": "amphetamine",
    "Amphetamines": "amphetamines",
    "Amphetamines (AMP)": "amphetamines-amp",
    "Amphetamines (MET)": "amphetamines-met",
    "Antidepressants": "antidepressants",
    "Barbiturates": "barbiturates",
    "Benzodiazepines": "benzodiazepines",
    "Buprenorphine": "buprenorphine",
    "Butorphanol": "butorphanol",
    "Carisoprodol": "carisoprodol",
    "Chromate": "chromate",
    "Cocaine": "cocaine",
    "Cotinine": "cotinine",
    "Ethanol Breath": "ethanol-breath",
    "Ethanol Urine": "ethanol-urine",
    "Fentanyl": "fentanyl",
    "Hydrocodone": "hydrocodone",
    "Hydrocodone/Hydromorphone": "hydrocodone-hydromorphone",
    "Ketamine": "ketamine",
    "Marijuana": "marijuana",
    "MDMA/MDA": "mdma-mda",
    "Meperidine": "meperidine",
    "Meprobamates": "meprobamates",
    "Methadone": "methadone",
    "Methamphetamine": "methamphetamine",
    "Methamphetamines": "methamphetamines",
    "Methaqualone": "methaqualone",
    "Nalbuphine": "nalbuphine",
    "Naltrexone": "naltrexone",
    "Nicotine": "nicotine",
    "Opiates": "opiates",
    "Oxycodone": "oxycodone",
    "Oxycodone/Oxymorphone": "oxycodone-oxymorphone",
    "Oxymorphone": "oxymorphone",
    "PCP": "pcp",
    "Pentazocine": "pentazocine",
    "Propoxyphene": "propoxyphene",
    "Specific Gravity": "specific-gravity",
    "Stimulants": "stimulants",
    "Synthetic Opiates": "synthetic-opiates",
    "Tramadol": "tramadol",
    "Tricyclics": "tricyclics",
    "Zolpidem (Ambien)": "zolpidem-ambien",
    # New items custom added for migration purpose 
    "Zolpidem - Ambien": "zolpidem-ambien",
    "Methadone Oral Fluid": "methadone",
    "Benzodiazepines Oral Fluid": "benzodiazepines",
    "Barbiturates Quantisal Oral Fluid": "barbiturates",
    "Marijuana Oral Fluid": "marijuana",
    "Oxycodone/Oxymorphone Oral Fluid": "oxycodone-oxymorphone",
    "Methamphetamine Oral Fluid": "methamphetamine",
    "Methamphetamine Isomers Oral Fluid": "methamphetamine",
    "Cocaine Oral Fluid": "cocaine",
    "AmphetamiAmphetamine Oral Fluid": "amphetamine",
    ## more to check and add
}

mapping_data = {key.upper(): value for key, value in row_data.items()}


# Function to get the mapped value
def get_mapped_value(input_string, no_mapping):
    mapping_data_upper = {key.upper(): value for key, value in mapping_data.items()}

    textToProcess = input_string.strip().upper().replace(" / ", "/").replace(" /\n", "/")
    result = mapping_data.get(textToProcess)

    if result:
        return result
    else:
        print(textToProcess)
        if textToProcess not in no_mapping:
            no_mapping.append(textToProcess)

        return "N/A"