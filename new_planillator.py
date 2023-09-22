#!/usr/bin/env PYTHONV

import csv
from datetime import date
from shutil import copyfile
import sys

src_file = sys.argv[2]
dst_file = sys.argv[1]
# delimiter = sys.argv[??]
id_colname = "id"
delimitador = ","
err = 0


class dataframe:
    def __init__(self, csv_file):
        with open(csv_file, newline='') as csvfile:
            datareader = csv.reader(csvfile, delimiter = delimitador, quotechar='"')
            rows = [row for row in datareader]

        self.filename = csv_file
        self.header = rows[0]
        self.features = self.header[1:] # Aca hay un problema: si el ID no es la primera columna, cagamos. Pero quien demonios no lo pondria primero
        self.body = rows[1:]
        self.id_col_index = self.header.index(id_colname) 
        self.id_vector = [i[self.id_col_index] for i in self.body]


# Funciones para el merge
def find_row(dataframe, id_num):
    """En cuentra una fila en un dataframe segun numero de ID."""
    i = 0
    for row in dataframe.body:
        if row[dataframe.id_col_index] == id_num:
            return row
        else:
            i += 1
    return None


def fill_with_NA(dataframe):
    """Chequea que la longitud de cada fila sea igual al header. 
    Es decir, que para cada variable (feature) haya un valor en cada columna.
    Si ese no valor no existe ya, rellena con NA."""
    for row in dataframe.body:
        n_missing_rows = len(dataframe.header) - len(row)
        while n_missing_rows != 0:
            row.append("NA")
            n_missing_rows -= 1

       
old_data = dataframe(sys.argv[1])
input_data = dataframe(sys.argv[2])


# Chequear errores:
# 1. Que no haya IDs repetidos en new_id_vector
unique_ids = set(input_data.id_vector)
if len(unique_ids) != len(input_data.id_vector):
    print("Error: IDs repetidos")
    # Agregar detalle de cuales son
    exit(1)

# 2. Todos los nuevos IDs deben estar incluidos en los viejos IDs. No se acepta agregar nuevos ids.
alien_ids = [i for i in input_data.id_vector if i not in old_data.id_vector]
if len(alien_ids) > 0:
    for i in alien_ids:
        print(f'Error en archivo source: el ID {i} no esta incluido en los IDs del archivo destino')
    exit(1)


# 3. Todas las filas deben tener la misma longitud
for row in input_data.body:
    if len(row) != len(input_data.header):
        print(f'Error: fila en archivo source con distinta cantidad de columnas que las demás:\n {row}')
        err = 1

    if err != 0:
        exit (1)


# --- Merged data frame
class MergedDataFrame:
    def __init__(self, header, body):
        self.filename = "none"
        self.header = header
        self.body = body
        self.id_col_index = self.header.index(id_colname)
        self.id_vector = [i[self.id_col_index] for i in self.body]

    def input(self, feature, value):
        feature_index = self.header.index(feature)
        

# Merged header
alien_features = [i for i in input_data.features if i not in old_data.features]
merged_header = old_data.header.copy()
if len(alien_features) > 0:
    for i in alien_features:
        merged_header.append(i)

# Merged body
merged_body = old_data.body.copy()

# Merged data frame
merged_df = MergedDataFrame(merged_header, merged_body)
fill_with_NA(merged_df)


# Tiene que pasar: id, feature y value
while len(input_data.features) != 0:
    feature = input_data.features.pop()
    f_index = input_data.header.index(feature)

    i = 1
    for input_row in input_data.body:
        entry_id = input_row[input_data.id_col_index]
        entry_value = input_row[f_index]

        target_row = find_row(merged_df, entry_id)
        if target_row is None:
            print(f'Error al tratar de hacer merge. El id {entry_id} no existe.')
            exit(1)
        target_index = merged_df.header.index(feature)

        if target_row[target_index] == "NA" or target_row[target_index] == "":
            target_row[target_index] = entry_value
            print(f'\t{i}  ID: {entry_id}\t{feature} --> {target_row[target_index]}')
            i += 1
        else:
            print(f'Error: se intentó sobre-escribir la variable {feature} en el ID {entry_id}')
            err = -1


# Abort in case of error
if err != 0:
    exit (1)


# Create back-up
today = date.today()
fmt_date = "{}-{}-{}".format(today.year, today.month, today.day)
bak_name = old_data.filename + "_"  + fmt_date + ".bak"
copyfile(old_data.filename, bak_name)
print(f'\nSe creo back-up:   {bak_name}')

# Save updated csv
with open(old_data.filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=delimitador,
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(merged_df.header)
    for row in merged_df.body:
        writer.writerow(row)
print(f'Se actualizo:   {old_data.filename}')        
