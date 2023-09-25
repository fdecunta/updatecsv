#!/usr/bin/env PYTHONV

import argparse
import csv
from datetime import date
from os import path
from shutil import copyfile
import sys

prog_description = "updatecsv"
# delimiter = sys.argv[??]
id_colname = "id"
delimitador = ","
error_code = 0           

class DataFrame:
    def __init__(self, csv_file):
        """Read a csv file and represents it as a dataframe."""

        # Check if csv_file exists and is a regular file
        if path.isfile(csv_file) is False:
            print(f'Error: no existe el archivo {csv_file}')
            exit(3)

        # Read the csv file
        with open(csv_file, newline='') as csvfile:
            datareader = csv.reader(csvfile, delimiter = delimitador, quotechar='"')
            rows = [row for row in datareader]

        # Attributes
        self.filename = csv_file 
        self.header = rows[0]   # The first row must be the header row with the variables names
        self.body = rows[1:]            # The body which contains all the observations
        # ????
        self.features = self.header[1:] # TODO!!!: Aca hay un problema: si el ID no es la primera columna, cagamos. Pero quien demonios no lo pondria primero

        # Search for the ID column and raise an error if it doesn't exists
        try:
            self.id_col_index = self.header.index(id_colname) # Index of the ID column in the header list
        except:
            print(f'Error: no se encontro la columna "{id_colname}" en el archivo {path.basename(self.filename)}')
            exit(2)
            
        self.id_vector = [i[self.id_col_index] for i in self.body] # Vector with all the IDs in the file


class MergedDataFrame:
    """Represents a new dataframe. Includes the information of the old
    and input data frames."""
    def __init__(self, header, body):
        self.filename = "none"
        self.header = header
        self.body = body
        self.id_col_index = self.header.index(id_colname)
        self.id_vector = [i[self.id_col_index] for i in self.body]

    def input(self, feature, value):
        feature_index = self.header.index(feature)

# ----------------------------------------    

def check_errors(old_data, input_data):
    """Checks for possible errors and inconsistencies in the data frames """
    global error_code 

    # 1. Input data should not have repeated IDs.
    repeated_ids = [rep_id for rep_id in input_data.id_vector if input_data.id_vector.count(rep_id) > 1] 
    if len(repeated_ids) > 0:
        print("Error: IDs repetidos en el archivo input")
        print(repeated_ids)
        error_code = 1

    # 2. All the new IDs must be included in the old IDs. Adding new IDs is not allowed.
    alien_ids = [id_num for id_num in input_data.id_vector if id_num not in old_data.id_vector]
    if len(alien_ids) > 0:
        for alien_id in alien_ids:
            print(f'Error: ID {alien_id} del archivo input no existe en archivo destino')
            error_code = 1

    # 3. All rows should have the same length (number of elements).
    for row in input_data.body:
        if len(row) != len(input_data.header):
            print(f'Error: fila en archivo input con distinta cantidad de columnas que las demás:\n {row}')
            error_code = 1

    if error_code != 0:
        print("No se realizaron cambios.")
        exit(1)


# Auxiliary functions for the merge
def find_row(dataframe, id_num):
    """Find and return a row in a dataframe based on ID number.
    Return None if fails."""
    for row in dataframe.body:
        if row[dataframe.id_col_index] == id_num:
            return row
    return None


def fill_with_NA(dataframe):
    """Compares the length of each row with the length of the header.
    Each observation should have the same number of elements as the
    header.  If any element is missing, it is filled with NA."""
    for row in dataframe.body:
        n_missing_rows = len(dataframe.header) - len(row)
        while n_missing_rows != 0:
            row.append("NA")
            n_missing_rows -= 1

       
def merge_dataframes(old_data, input_data):
    """Creates a merged data frame from two data frames, taking care
    not to overwrite any values"""

    global error_code 

    # 1. Merged header
    """Merge the header from the two files. New columns from the input
    file are added if needed"""
    alien_features = [i for i in input_data.features if i not in old_data.features]
    merged_header = old_data.header.copy()
    if len(alien_features) > 0:
        for feature in alien_features:
            merged_header.append(feature)

    # 2. Template body without new values
    """Creates the merged file's body using the old data. If new
    columns were added from the input data, it fills each row with NA"""
    merged_body = old_data.body.copy()
    merged_df = MergedDataFrame(merged_header, merged_body)
    fill_with_NA(merged_df)

    # 3. Add the new values
    """Updates the merged body with new values, one feature (variable)
    at a time from the input data. For each row in the input data, it
    locates the corresponding row in the merged data frame by the ID
    number and adds the new value to the respective feature. It raises
    a warning if the new value is empty and raises an error in the
    following cases:

       - If the ID does not exist (although this is unlikely due to prior
checking)
       - If an attempt is made to overwrite an existing value."""

    while len(input_data.features) != 0:
        feature = input_data.features.pop() # Take one feature at a time until the list is empty
        f_index = input_data.header.index(feature) # Find the feature index to reach the new value in each row

        line = 1                # Line number for printing in the terminal
        for input_row in input_data.body:
            # For each row find the ID and the value corresponding to the current feature
            entry_id = input_row[input_data.id_col_index]
            entry_value = input_row[f_index]

            if len(entry_value) == 0:
                """If the entry value is empty raise a warning but
                don't stop the program, just skip"""
                print(f'Warning: no value in the ID {entry_id} for the {feature} variable in input data. No value added')
                continue

            target_row = find_row(merged_df, entry_id)
            if target_row is None:
                # Check if ID exists in the merged data frame. This sould be OK but just for the case
                print(f'Error al tratar de hacer merge. El id {entry_id} no existe.')
                exit(1)
            target_index = merged_df.header.index(feature)

            if target_row[target_index] == entry_value:
                # Skip if the new value is the same as the old value
                continue
            elif target_row[target_index] == "NA" or target_row[target_index] == "":
                # Don't overwrite existing data. 
                target_row[target_index] = entry_value
                print(f'\t{line}  ID: {entry_id}\t{feature} --> {target_row[target_index]}')
                line += 1
            else:
                print(f'Error: se intentó sobre-escribir la variable {feature} en el ID {entry_id}')
                error_code = -1

    # Abort in case of error before make any change
    if error_code != 0:
        exit (1)

    # 4. Create back-up file with the old dataframe.
    today = date.today()
    bak_name = f'{old_data.filename}_{today.isoformat()}.bak'
    copyfile(old_data.filename, bak_name)
    print(f'\nSe creo back-up:   {bak_name}')

    # 5. Save the updated csv
    with open(old_data.filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimitador,
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(merged_df.header)
        writer.writerows(merged_df.body)
    print(f'Se actualizo:   {old_data.filename}')        

    
# ----------------------------------------    

def main():
    parser = argparse.ArgumentParser(prog = 'planillator',
                                     description = prog_description)
    parser.add_argument('-s',
                        action = 'store_true',
                        default = False,
                        dest = "sflag",
                        help ='Define el separador (coma por default)')
    parser.add_argument('-d',
                        action = 'store_true',
                        default = False,
                        dest = "dflag",
                        help = 'dry-run. Realiza el merge sin guardar cambios')

    parser.add_argument('old_data')
    parser.add_argument('input_data')

    options = parser.parse_args()

    old_data = DataFrame(options.old_data)
    input_data = DataFrame(options.input_data)

    check_errors(old_data, input_data)
    merge_dataframes(old_data, input_data)
    exit(0)


if __name__ == '__main__':
    main()    
