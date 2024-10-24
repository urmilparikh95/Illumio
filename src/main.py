import argparse
import os.path
import csv
from log_processor import LogProcessor

PROTOCOL_FILE_PATH = "data/protocol-numbers-1.csv"
TAG_COUNT_FILE = "tag_counts.out"
COMBO_COUNT_FILE = "combo_counts.out"

def generate_protocol_map() -> dict:
    protocol_map = {}
    with open(PROTOCOL_FILE_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Keyword"] != "":
                protocol_map[row["Decimal"]] = row["Keyword"].lower()
    return protocol_map

def generate_lookup_table(path, protocol_map) -> dict:
    lookup_table = {}
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dstport = row.get("dstport", None)
            protocol = row.get("protocol", None)
            tag = row.get("tag", None)
            if not dstport or not protocol or not tag:
                return None, "Missing field in CSV file contents."
            if not dstport.isdigit():
                return None, "Invalid dstport in CSV file contents."
            if protocol == "":
                return None, "Invalid protocol number in CSV file contents."
            if tag == "" or tag.isdigit():
                return None, "Invalid tag in CSV file contents."
            # key is a tuple containing dstport and protocol
            lookup_table[(dstport, protocol.lower())] = tag
    return lookup_table, None


def main():
    parser = argparse.ArgumentParser(
        description="Script to Process Flow Logs.",
        epilog="If no --custom param specified, it assumes the log format is default log."
    )
    parser.add_argument("-l", "--logfile", help="File path for the flow log file. (REQUIRED)", required=True)
    parser.add_argument("-c", "--csv", help="File path for the lookup csv file. (REQUIRED)", required=True) 
    parser.add_argument("--custom", help="0 indexed column indices for dest port and protocol passed as a space separated string.")

    args = parser.parse_args()

    # Validate Inputs
    log_file = args.logfile
    if not os.path.isfile(log_file):
        print(f"Invalid log file path: {log_file}.")
        return

    csv_file = args.csv
    if not os.path.isfile(log_file):
        print(f"Invalid CSV file path: {csv_file}.")
        return

    # Get column index for dstport and protocol in log files. 
    # 6 and 7 are column index for dstport and protocol in default logs.
    # Update them for custom logs if present.
    dstport_column_index = 6
    protocol_column_index = 7
    if args.custom:
        custom_colums = args.custom.split(" ")
        if len(custom_colums) != 2 or not custom_colums[0].isdigit() or not custom_colums[1].isdigit():
            print(f"Invalid custom file column indices: {args.custom}.")
            return
        dstport_column_index = int(custom_colums[0])
        protocol_column_index = int(custom_colums[1])
    
    # Create a mapping for protocol number to protocol keyword
    protocol_map = generate_protocol_map()
    # Create a lookup table as a dictionary (hashmap).
    lookup_table, error = generate_lookup_table(csv_file, protocol_map)
    if error:
        print("Error:", error)
        return
    
    # Create instance of Log Processor
    log_processor = LogProcessor(lookup_table)

    # Read input SSV log file
    with open(log_file, "r") as file:
        for line in file:
            keywords = line.split(" ")

            # Skip invalid log line
            if len(keywords) < max(dstport_column_index, protocol_column_index) + 1:
                continue

            dstport = keywords[dstport_column_index]
            protocol = protocol_map[keywords[protocol_column_index]]

            # Send data to log processor
            log_processor.add_data(dstport, protocol)
    
    # Generate the two output files
    log_processor.write_tag_count_file(TAG_COUNT_FILE)
    log_processor.write_combo_count_file(COMBO_COUNT_FILE)
        

if __name__=="__main__":
    main()