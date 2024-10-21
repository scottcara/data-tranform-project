import pandas as pd
from config import OPENAI_API_KEY 
from openai import OpenAI
import re
from pprint import pprint

# Read the CSV files
df_source = pd.read_csv('/Users/scottcara/Documents/VSCode/data-transform-project/data/source_file.csv')
df_destination = pd.read_csv('/Users/scottcara/Documents/VSCode/data-transform-project/data/destination_file.csv')


# Use only chat completion to try to match the columns. It's doing a bad job even when forcing things
def generate_header_match(source_dataset, destination_header, destination_dataset):
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"Please suggest the best header in {source_dataset} for {destination_header}, which is a header in {destination_dataset}." \
            "Please also calculate your confidence score in this match." \
            "Please return the response as follows: 'Best match: header name. Confidence: % confidence score. And then explain why you chose that header"
#    print(prompt)
    # Use the new ChatCompletion method
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo" if you prefer
        messages=[
        {"role": "system", "content": "You are a tool that transforms data from one database to another."},
        {"role": "user", "content": prompt}
        ]
    )
    match = response.choices[0].message.content.strip()

    return match

# Set up dictionary to store the output
output_data = {}

# Loop over destination to generate the best match
for column in df_destination.columns[1:]:
    # Reset values
    best_match = None
    confidence_score = None
    print(column)
    # Generate the best match
    response = generate_header_match(df_source, column, df_destination)
    print(response)
    # Extract the best match and confidence score
    name_match = re.search(r'Best match: (\w+)', response)
    confidence_match = re.search(r'Confidence: (\d+)%', response)
    
    # Store the output
    if name_match:
        best_match = name_match.group(1)
        print(f"Best match: {best_match}")
    else:
        print("No name match found")

    if confidence_match:
        confidence_score = confidence_match.group(1)
        print(f"Confidence: {confidence_score}")
    else:
        print("No confidence match found")

    # Store the output
    output_data[column] = {
        "source_header": best_match,
        "confidence": confidence_score
    }

# Print the dictionary
pprint(output_data)