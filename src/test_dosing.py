# IMPORT MODULES
import pandas as pd

pd.options.mode.chained_assignment = None
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

    def test_merge(self):
        """
        :return: merged dataframe.
        """
        df = pd.merge(self.df1, self.df2, on=['RID', 'VISCODE'], how='left')
        return df

    def test_filter(self, df):
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


# Test merge length and filter length with valid properties
def test_valid_action():
    gen = REPORTGEN(df1="../dm-code-challenge/t2_registry 20190619.csv",
                    df2="../dm-code-challenge/t2_ec 20190619.csv",
                    VISCODE="w02",
                    SVDOSE="Y",
                    ECSDSTXT=280, dir_to_write="../dm-code-challenge/")
    assert len(gen.test_merge()) >= 1
    merged_df = gen.test_merge()
    assert len(gen.test_filter(merged_df)) >= 1


# Test merge length and filter with VISCODE set to "w04".


def test_invalid_action():
    gen = REPORTGEN(df1="../dm-code-challenge/t2_registry 20190619.csv",
                    df2="../dm-code-challenge/t2_ec 20190619.csv",
                    VISCODE="w12",
                    SVDOSE="Y",
                    ECSDSTXT=200, dir_to_write="../dm-code-challenge/")

    assert len(gen.test_merge()) == 14
    merged_df = gen.test_merge()
    # Filter will be 0 as setting ECSDSTXT to '200' produces no valid results.
    assert len(gen.test_filter(merged_df)) == 0


# Invalid data types
def test_invalid_type():
    gen = REPORTGEN(df1="../dm-code-challenge/t2_registry 20190619.csv",
                    df2="../dm-code-challenge/t2_ec 20190619.csv",
                    VISCODE="w04",
                    SVDOSE="Y",
                    ECSDSTXT="200", dir_to_write="../dm-code-challenge/")
    merged_df = gen.test_merge()
    gen.test_filter(merged_df)
    assert type(gen.ECSDSTXT) is int


if __name__ == "__main__":
    # Test for length with valid properties
    test_valid_action()

    # test for length with invalid properties
    test_invalid_action()

    # test with invalid data type
    test_invalid_type()
