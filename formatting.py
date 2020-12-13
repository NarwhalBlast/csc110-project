import xlrd
import csv
from typing import Tuple, List, Dict, Any

# Usable data
#
# This is in the form of Tuple[datetime.datetime, List[Any]]
# (start_year, [value1, value2, value3, value4])


def xlsx_to_data(filename: str) -> Dict[int, Any]:
    """ Convert the xlsx file to usable data.
    """
    # opening workbook and accessing the 2nd sheet
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(1)
    num_rows = sheet.nrows
    num_cols = sheet.ncols

    # ACCUMULATOR: stores the data extracted from the xlsx file
    data_so_far = {}
    for i in range(3, num_rows):
        # determine if it is necessary for the corresponding value to be a list
        if num_cols > 2:
            data_so_far[int(sheet.cell(i, 0).value)] = []

        for j in range(1, num_cols):
            cell_value = sheet.cell(i, j).value
            key = int(sheet.cell(i, 0).value)
            # if the corresponding value is a list
            if num_cols > 2 and isinstance(cell_value, (int, float)):
                data_so_far[key].append(cell_value)
            # if the corresponding value is just a number
            elif isinstance(cell_value, (int, float)):
                data_so_far[key] = cell_value

    return data_so_far


def csv_to_data(filename: str) -> Dict[int, Any]:
    """ Convert the csv file to usable data.
    """
    with open(filename) as file:
        reader = csv.reader(file)
        # skip the first line
        next(reader)
        # ACCUMULATOR: stores the data extracted from the csv file
        data_so_far = {}
        for row in reader:
            year = int(row[0][0:4])
            # if the first column is already stored in yyyy format
            if len(row[0]) == 4:
                data_so_far[year] = float(row[1])
            # if the first column is in yyyy-mm-dd format
            elif (year in data_so_far) and row[1] != '':
                data_so_far[year].append(float(row[1]))
            elif row[1] != '':
                data_so_far[year] = [float(row[1])]

    return data_so_far


def add_red_list_species(data: Dict[int, list]) -> None:
    """ Add the number of vertebrates, invertebrates, plants, and fungi & protists on the red list
    together for each year. This function mutates the input data.
    """
    for key in data:
        data[key] = sum(data[key])


def dict_to_tuple_of_lists(data: Dict[int, float]) -> Tuple[List[int], List[float]]:
    """ Returns a tuple of two lists. The first list contains the years (the keys of the input dictionary) and the
    second list contains the actual data values (the corresponding values of the input dictionary)
    """
    x_values = [key for key in data]
    y_values = [data[key] for key in data]
    return (x_values, y_values)


def tuple_to_dict(data: Tuple[List[int], List[float]]) -> Dict[int, float]:
    """ Return a mapping of years to the corresponding value.
    """
    data_so_far = {}
    for i in range(0, len(data[0])):
        data_so_far[data[0][i]] = data[1][i]

    return data_so_far
