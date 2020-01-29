# IMPORT MODULES
import pandas as pd

pd.options.mode.chained_assignment = None
import argparse
import plotly.express as px
import os

# Set variable.
# Path to the registry csv
PATH_TO_CSV = "../dm-code-challenge/t2_registry 20190619.csv"
# Query to filter the frame
QUERY = 'VISCODE not in ["bl"] and SVPERF in ["Y"]'
# Title of the plot
TITLE = "Viscodes from Registry"
# Group by sector
NAMES = 'VISCODE'
# Filename of the report
filename = "results.csv"


# Utility method to check for dir_path.
def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(f"readable_dir:{path} is not a valid path")


class PICHART:
    """
    Class to generate Pichart
    """

    def __init__(self, path_to_csv, query, title, names):
        """

        :param path_to_csv: Registry CSV
        :param query: Query to filter the frame
        :param title: Title of the plot
        :param names: Group by sector
        """
        self.path = path_to_csv
        self.query = query
        self.title = title
        self.names = names

    def genchart(self):
        """
        :return: Generated plot.
        """
        df = pd.read_csv(self.path)
        df = df.query(self.query)
        fig = px.pie(df, names=self.names, title=self.title)
        return fig.show()


class REPORTGEN:
    """
    Class declaration for report generation.
    """

    def __init__(self, df1, df2, VISCODE, SVDOSE, ECSDSTXT, dir_to_write):
        """
        :param df1: The dataframe 1 from registry
        :param df2:  The dataframe 2
        :param VISCODE:
        :param SVDOSE:
        :param ECSDSTXT:
        :param dir_to_write:
        """
        self.df1 = df1
        self.df2 = df2
        self.VISCODE = VISCODE
        self.SVDOSE = SVDOSE
        self.ECSDSTXT = ECSDSTXT
        self.dir_to_write = dir_to_write
        self.read_frames()

    def read_frames(self):
        """
        Read the path to the files as a pandas dataframe
        """
        self.df1 = pd.read_csv(self.df1)
        self.df2 = pd.read_csv(self.df2)

    def _merge(self):
        """
        :return: merged dataframe.
        """
        df = pd.merge(self.df1, self.df2, on=['RID', 'VISCODE'], how='left')

        if len(df.index) <= 1:
            raise ValueError(" Merge didn't materialize result")
        return df

    def _filter(self, df):
        """
        :param df: input to be filtered.
        :return: filterd dataframe processes by business logic.
        """
        if not isinstance(self.ECSDSTXT, (int, float)):
            raise TypeError("ECSDSTXT, expected to be type 'int' ")

        if not all(isinstance(i, str) for i in [self.VISCODE, self.SVDOSE]):
            raise TypeError("Expected of type 'str' ")
        df = df[
            (df.VISCODE == self.VISCODE) & (df.SVDOSE == self.SVDOSE)
            & (df.ECSDSTXT != self.ECSDSTXT)]

        if len(df.index) <= 1:
            raise ValueError(" Filter didn't materialize result")

        return df

    def _write_csv(self, df):
        """
        :param df: input dataframe
        :return: nothing.
        """
        df = df[['ID', 'RID', 'USERID', 'VISCODE', 'SVDOSE', 'ECSDSTXT']]
        df.to_csv(self.dir_to_write + '/' + "results.csv", index=False)

    def _drop_y(self, df):
        """
        :param df: input dataframe to drop duplicates series
        during merge collisions attributed due to the same column names.
        in the data frames.
        :return:
        """
        # list comprehension of the cols that end with '_y'
        to_drop = [x for x in df if x.endswith('_y')]
        df.drop(to_drop, axis=1, inplace=True)
        return df

    def _rename_x(self, df):
        """
        :param df: Rename columns that start with _x to raw data
        column names
        :return:
        """
        for col in df:
            if col.endswith('_x'):
                df.rename(columns={col: col.rstrip('_x')}, inplace=True)
        return df


if __name__ == "__main__":
    # Parser for the report generation.

    parser = argparse.ArgumentParser(
        description='A utility to create csv report')

    parser.add_argument("--VISCODE", default='w02', type=str,
                        help=" 'VISCODE' set variable to filter report generation.")

    parser.add_argument("--SVDOSE", default='Y', type=str,
                        help=" 'SVDOSE' set variable to filter report generation")

    parser.add_argument("--ECSDSTXT", default=280, type=int,
                        help=" 'ECSDSTXT' set variable to filter report generation")

    parser.add_argument("--path", default="../dm-code-challenge/",
                        type=dir_path,
                        help=" 'path' set  variable to write report to directory")
    args = parser.parse_args()

    gen = REPORTGEN(
        df1="../dm-code-challenge/t2_registry 20190619.csv",
        df2="../dm-code-challenge/t2_ec 20190619.csv",
        VISCODE=args.VISCODE,
        SVDOSE=args.SVDOSE,
        ECSDSTXT=args.ECSDSTXT,
        dir_to_write=args.path
    )
    # Step 1- Merge
    merged_df = gen._merge()
    # Step 2 - Filter
    filtered_df = gen._filter(merged_df)
    # Step 3 - Drop columns
    drop_df = gen._drop_y(filtered_df)
    # Step 4 - Rename columns
    rename_df = gen._rename_x(drop_df)
    # Step 5 - Write CSV
    gen._write_csv(rename_df)

    #  Create Instance of PICHART class
    registry = PICHART(PATH_TO_CSV, QUERY, TITLE, NAMES)
    # Generate PICHART on the class instance.
    registry.genchart()
