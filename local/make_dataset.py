import os
from datetime import datetime

class DatasetMerger:
    def __init__(self, datasets, output_dir='dataset'):
        self.datasets = datasets
        self.output_dir = output_dir
        self.merged_data = ''

    def read_and_merge(self):
        """Read and merge the contents of all dataset files."""
        for dataset in self.datasets:
            with open(dataset, 'r') as file:
                self.merged_data += file.read()

    def write_to_file(self):
        """Write the merged data to a timestamped JSON file in the output directory."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Generate a timestamped filename
        output_file = os.path.join(self.output_dir, f'data.json')
        
        # Write the merged data to the file
        with open(output_file, 'w') as file:
            file.write(self.merged_data)

    def merge_and_save(self):
        """Execute the process of merging and saving the dataset."""
        self.read_and_merge()
        self.write_to_file()

datasets = ['roleplay.json', 'python.json']  # Input your dataset filenames here
merger = DatasetMerger(datasets)
merger.merge_and_save()