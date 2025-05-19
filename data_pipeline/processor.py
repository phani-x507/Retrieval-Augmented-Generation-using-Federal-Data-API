import json

def process_data():
    with open("raw_data.json", "r") as f:
        data = json.load(f)

    processed_data = []
    for item in data.get("results", []):
        record = {
            "title": item.get("title"),
            "summary": item.get("abstract"),
            "publication_date": item.get("publication_date"),
            "agency": item.get("agency_names", ["Unknown"])[0]
        }
        processed_data.append(record)

    with open("processed_data.json", "w") as f:
        json.dump(processed_data, f)
    print("Data processed successfully.")

process_data()
