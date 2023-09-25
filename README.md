# updatecsv

This is a command-line program that merges two CSV files based on a specific column ("id" column by default). It adds new values without overwriting the old ones.

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

## Installation

```shell
git clone https://github.com/fdecunta/new-planillator.git
cd new-planillator
sudo make install
```

To remove the program:

```shell
cd new-planillator
sudo make uninstall
```

