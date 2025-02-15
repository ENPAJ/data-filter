from rich.console import Console
from rich.table import Table
import os


def read_file(file_path, sep=",", encoding="utf-8"):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".csv":
        return read_csv(file_path, sep=sep, encoding=encoding)
    elif ext == ".json":
        return read_json(file_path)
    elif ext in [".yaml", ".yml"]:
        return read_yaml(file_path)
    elif ext == ".xml":
        return read_xml(file_path)
    else:
        raise ValueError("Format non supporté.")


def read_csv(file_path, sep=",", encoding="utf-8"):
    """Lecture du fichier csv, prend en compte les valeurs manquantes"""
    with open(file_path, mode='r', encoding=encoding) as f:
        lines = f.readlines()

    columns = lines[0].strip().split(sep)
    data = [line.strip().split(sep) for line in lines[1:]]
    
    # Gestion des valeurs manquantes
    for row in data:
        while len(row) < len(columns):
            row.append('')  # Remplit les valeurs manquantes par une chaîne vide
    
    return csv_data(columns, data)


class csv_data:
    def __init__(self, columns, data, sep=','):
        self.lines = data
        self.columns = columns
        
        # Data sous forme de dictionnaire
        self.data = {column: [] for column in self.columns}
        for row in self.lines:
            for index, column in enumerate(self.columns):
                self.data[column].append(row[index] if index < len(row) else '')

        # Détection des types de colonnes
        self.dtypes = {}
        for column in self.columns:
            self.dtypes[column] = self.list_type(column)
            if self.dtypes[column] == 'int':
                self.data[column] = list(map(lambda x: int(x) if x else None, self.data[column]))
            if self.dtypes[column] == 'float':
                self.data[column] = list(map(lambda x: float(x) if x else None, self.data[column]))

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.lines[key]
        if isinstance(key, str):
            return self.data[key]
        if isinstance(key, slice):
            return self.lines[key]

    def list_type(self, column):
        try:
            if self.data[column][0] == '':
                return None
            return type(eval(self.data[column][0])).__name__
        except:
            return 'str'

    def filter(self, col, condition):
        """Filtre les lignes en fonction d'une condition sur une colonne"""
        index = self.columns.index(col)
        filtered_data = [row for row in self.lines if condition(row[index])]
        return csv_data(self.columns, filtered_data)

    def export_csv(self, file_path, sep=",", encoding="utf-8"):
        """Export des données en CSV"""
        with open(file_path, mode='w', encoding=encoding) as f:
            f.write(sep.join(self.columns) + "\n")
            for row in self.lines:
                f.write(sep.join(map(str, row)) + "\n")
        print(f"Fichier exporté sous {file_path}")

    def head(self, n=5):
        console = Console()
        table = Table(show_header=True, header_style="bold cyan")

        for col in self.columns:
            table.add_column(col, justify="left", style="bold white")

        for i in range(min(n, len(self.lines))):
            row = [str(self.data[col][i]) for col in self.columns]
            table.add_row(*row)

        console.print(table)


# Exemple d'utilisation
cd = read_csv("D:\\Downloads\\iris.csv", sep=";")
filtered_cd = cd.filter("sepal_length", lambda x: float(x) > 5.0)
filtered_cd.export_csv("D:\\Downloads\\iris_filtered.csv")
cd.head()
