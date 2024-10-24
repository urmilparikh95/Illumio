from collections import defaultdict
import csv

class LogProcessor:
    """
    Main class to process logs.
    Maintains 2 dict:
    1. (dstport, protocol) is the key counts its occurances
    2. tag is the key and counts its occurances. Also counts the ones that are untagged
    Also has functions to write the output file.
    """
    def __init__(self, lookup_table):
        self.lookup_table = lookup_table
        self.tag_count = defaultdict(int)
        self.combo_count = defaultdict(int)
    
    def add_data(self, dstport, protocol):
        tag = self.lookup_table.get((dstport, protocol), "untagged")
        self.tag_count[tag] += 1
        self.combo_count[(dstport, protocol)] += 1
    
    def write_tag_count_file(self, output_file):
        fields = ["tag", "count"]
        with open(output_file, "w", newline="") as f:
            f.write("Tag Counts: \n\n")
        with open(output_file, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for tag in self.tag_count:
                writer.writerow({"tag": tag, "count": self.tag_count[tag]})
    
    def write_combo_count_file(self, output_file):
        fields = ["port", "protocol", "count"]
        with open(output_file, "w", newline="") as f:
            f.write("Port/Protocol Combination Counts: \n\n")
        with open(output_file, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for port, protocol in self.combo_count:
                writer.writerow({"port": port, "protocol": protocol, "count": self.combo_count[(port, protocol)]})