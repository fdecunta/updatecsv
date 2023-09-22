# Planillator

## Motivation

I work on conducting experiments with plants. When I take measurements from these plants (e.g., weigh their dry biomass), I rarely had a computer at hand, so I record the results with pen and paper. Afterward, I need to transfer these results to a spreadsheet along with other data, such as plant treatments and measurements of other variables.

Each plant is assigned an ID number. Sometimes, I can take measurements in the order of these ID numbers, which makes inputting the new data into the spreadsheet straightforward. However, this is rarely the case and measurements are taken without a specific order. In such cases, when I transfer the input data from the paper into the spreadsheet, I often find myself navigating up and down within the spreadsheet, searching for each ID, then going to the correct column and writing down the data. This process is horrible, time-consuming, and prone to errors.

The planillator try to solve this problem. I input the data into a spreadsheet exactly as it was recorded on paper. Then, the planillator merges this file with the rest of the data based on the ID and the column name.

## Usage

```bash
planillator old_data.csv input_data.csv
```

For example:

```bash
planillator experiment_2023.csv aboveground_biomass.csv
```

## Installation

I don't know
