# updatecsv

This is a minimal command-line utility to add data to a CSV file from another CSV file. This is done based on a specified column, which must contain unique identifiers (e.g., ID number). 

The program was designed for updating data frames with experiments data, where each row represents an experimental unit. Thus, it does not add new rows, and the identifiers in the input file must be a subset of those in the original file. Also, data from the original file cannot be overwritten.

The program creates a backup file, updates the original file, and prints the changes in the terminal.

## Features

- Safely add new values.
- Automatically creates a backup file for the original CSV.
- Flexible column separator.
- Customizable merge column.
- Dry-run mode for previewing changes without applying them.

## Usage 

```
updatecsv [OPTIONS] original_data.csv input_data.csv

Options:
  -s   [separator]    Specify the item separator in the csv files (default is comma)
  -d                  Dry-run with no changes made
  --by [column name]  Defines the column to use for the merge (default is id)
```

## Examples

Adding new data with default values (comma as separator, id as merge column):

```bash
updatecsv experiment_2023.csv aboveground_biomass.csv
```

Adding new deta with custom options (semicolon as the separator, dry-run mode, and a custom merge column named 'key'):


```bash
updatecsv -s ';' -d --by key experiment_2022.csv alkaloids.csv
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

