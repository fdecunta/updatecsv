# Planillator

Merge two CSV files by a column. If some column is duplicated, it add new values but without overwritting old values. 

I use it regularly to update data from experiments with new measures.

It works with only with CSV files because they are easier to manipulate and highly portable.

## Usage

```bash
planillator old_data.csv input_data.csv
```

For example:

```bash
planillator experiment_2023.csv aboveground_biomass.csv
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

