# updatecsv

This is a minimal command-line utility to update an existing CSV file with data from another CSV file. This is done based on a specified column, which must be a unique identifier. It allows you to add new columns and values without overwriting existing data.

The program creates a backup file, updates the original file, and prints the changes in the terminal.

I was design for updating data from experiments with new measurements.


## Features

- Safely add new values without overwriting existing data.
- Automatically creates a backup file for the original CSV.
- Flexible column separator.
- Customizable merge column.
- Dry-run mode for previewing changes without applying them.

## Usage 

```
updatecsv [OPTIONS] old_data.csv input_data.csv

Options:
  -s   [separator]    Specify the item separator in the csv files (default is comma)
  -d                  Dry-run with no changes made
  --by [column name]  Defines the column to use for the merge (default is id)
```

## Examples

Merging two CSV files with default values (comma as separator, id as merge column):

```bash
updatecsv experiment_2023.csv aboveground_biomass.csv
```

Merging with custom options (semicolon as the separator, dry-run mode, and a custom merge column named 'key'):


```bash
updatecsv -s ';' -d --by key old_data.csv input_data.csv
```




## Installation

```shell
git clone https://github.com/fdecunta/updatecsv.git
cd updatecsv
sudo make install
```

To remove the program:

```shell
cd updatecsv
sudo make uninstall
```

## Requirements

- Python 3.6+
- CSV library

