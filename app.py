import streamlit as st
import io
import pandas as pd

#########################################
# Original CSV Handling Code (modified) #
#########################################

def read_csv(file, sep=",", encoding='utf-8'):
    """
    Reads a CSV file and returns a csv_data object.
    The file argument can be a file path or a file-like object.
    """
    if hasattr(file, "read"):  # file-like object from streamlit uploader
        file.seek(0)
        f = io.TextIOWrapper(file, encoding=encoding)
        lines = f.readlines()
    else:
        with open(file, mode='r', encoding=encoding) as f:
            lines = f.readlines()
            
    # Get column names from the header and the remaining lines as data
    columns = lines[0].strip().split(sep)
    data = [line.strip().split(sep) for line in lines[1:]]
    return csv_data(columns, data)

class csv_data:
    def __init__(self, columns, data, sep=','):
        """
        Creates a csv_data object.
        Attributes:
         - lines: list of rows (each row is a list of values)
         - columns: list of column names
         - data: dictionary mapping each column to a list of its values
         - dtypes: dictionary of inferred data types for each column
        """
        self.lines = data
        self.columns = columns

        # Build the data dictionary (each column maps to a list of values)
        self.data = {}
        for index, column in enumerate(self.columns):
            self.data[column] = []
            for row in self.lines:
                # If a row has fewer columns, add an empty string
                if index < len(row):
                    self.data[column].append(row[index])
                else:
                    self.data[column].append("")

        # Infer types and, if possible, convert values
        self.dtypes = {}
        for column in self.columns:
            self.dtypes[column] = self.list_type(column)
            if self.dtypes[column] == 'int':
                try:
                    self.data[column] = list(map(int, self.data[column]))
                except Exception as e:
                    pass
            elif self.dtypes[column] == 'float':
                try:
                    self.data[column] = list(map(float, self.data[column]))
                except Exception as e:
                    pass

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.lines[key]
        if isinstance(key, str):
            return self.data[key]
        if isinstance(key, slice):
            # Not implemented; you can add slicing if needed.
            pass

    def list_type(self, column):
        """
        Infer the type of the values in a column.
        Tries int first, then float, then falls back to string.
        """
        if self.data[column][0] == '':
            return None
        try:
            int(self.data[column][0])
            return 'int'
        except:
            pass
        try:
            float(self.data[column][0])
            return 'float'
        except:
            pass
        return 'str'

    def types(self):
        """Display the types of each column."""
        st.write("### Column Data Types")
        for column, typ in self.dtypes.items():
            st.write(f"- **{column}**: {typ}")

    def describe(self):
        """
        Provides simple numeric statistics (sum, mean, min, max) for each numeric column.
        Returns a dictionary of statistics.
        """
        stats = {}
        for column in self.columns:
            if self.dtypes[column] in ['int', 'float']:
                col_data = self.data[column]
                stats[column] = {
                    'sum': sum(col_data),
                    'mean': sum(col_data) / len(col_data),
                    'min': min(col_data),
                    'max': max(col_data)
                }
        return stats

    def sort(self, cols, ascending=True, inplace=False):
        """
        Sorts the data by the specified column(s).
        Note: Sorting is done on the raw lines (strings), and then the column
        data is rebuilt from these sorted rows.
        """
        if isinstance(cols, str):
            cols = [cols]

        indices = [self.columns.index(col) for col in cols]
        self.lines.sort(key=lambda x: tuple(x[i] for i in indices), reverse=not ascending)
        # Rebuild the data dictionary based on the sorted lines.
        for i, col in enumerate(self.columns):
            self.data[col] = [row[i] if i < len(row) else "" for row in self.lines]

    def head(self, n=5):
        """
        Returns the first n rows as a pandas DataFrame for display.
        """
        head_rows = self.lines[:n]
        return pd.DataFrame(head_rows, columns=self.columns)

##############################
# Streamlit App Starts Here  #
##############################

def main():
    st.title("CSV Data Explorer")
    st.write("Upload a CSV file to explore and sort your data.")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    sep = st.text_input("CSV Separator", value=",")

    if uploaded_file is not None:
        # Read the CSV into our csv_data object
        cd = read_csv(uploaded_file, sep=sep)

        st.subheader("Data Preview")
        # Display the first 10 rows using Streamlit's dataframe viewer.
        st.dataframe(cd.head(10))

        st.subheader("Column Data Types")
        # Display the data types
        cd.types()

        # Optionally, show a numeric description of the data.
        if st.checkbox("Show Numeric Description"):
            stats = cd.describe()
            if stats:
                st.write("### Numeric Description")
                st.write(stats)
            else:
                st.write("No numeric columns found.")

        st.subheader("Sort Options")
        # Allow user to select columns for sorting
        sort_columns = st.multiselect("Select column(s) to sort by", options=cd.columns)
        sort_order = st.radio("Sort order", options=["Ascending", "Descending"])
        if st.button("Sort Data"):
            if sort_columns:
                ascending = (sort_order == "Ascending")
                cd.sort(sort_columns, ascending=ascending)
                st.success("Data sorted!")
                st.dataframe(cd.head(10))
            else:
                st.error("Please select at least one column to sort by.")

if __name__ == "__main__":
    main()
