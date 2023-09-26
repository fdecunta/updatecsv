# updatecsv

This is a command-line program that merges two CSV files based on a specific column. It adds new values without overwriting the old ones.

I use this regularly to update data from experiments with new measurements.

It's designed to work exclusively with CSV files because they're easy to handle and highly portable.

## Usage

```bash
updatecsv old_data.csv input_data.csv
```

For example:

```bash
updatecsv experiment_2023.csv aboveground_biomass.csv
```

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

