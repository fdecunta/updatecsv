# updatecsv

This is a minimal command-line utility designed to merge two CSV files based on a specific column, allowing you to add new values without overwriting existing ones.

I found it useful for updating data from experiments with new measurements.

### Features

- Merge two CSV files based on a specified column.
- Safely add new values without overwriting existing data.
- Flexible column separator.
- Customizable merge column.
- Dry-run mode for previewing changes without applying them.


## Usage 

```bash
updatecsv [OPTIONS] old_data.csv input_data.csv
```

### Examples

Merging two CSV files without specifying options:

```bash
updatecsv experiment_2023.csv aboveground_biomass.csv
```

Merging with custom options (semicolon as the separator, dry-run mode, and a custom merge column named 'key'):


```bash
updatecsv -s ';' -d --by key old_data.csv input_data.csv
```

The program creates a backup file, updates the original file, and prints the changes in the terminal.


### Options

```
  -s   [separator]    Specify the item separator in the csv files (default is comma)
  -d                  Dry-run with no changes made
  --by [column name]  Defines the column to use for the merge (default is id)
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

