"""
Interface to read and write CSV data from and to S3.
"""
import pandas as pd
from pandas import DataFrame


class S3:
    """
    Facilitates transferring data between step function states.
    """
    
    def __init__(self, bucket: str, key_read: str, folder_write: str):
        self.bucket = bucket
        self.key_read = key_read
        self.folder_write = folder_write

    def read(self) -> DataFrame:
        """
        Read CSV file from S3 into a DataFrame

        :return: The CSV file as a DataFrame
        """
        df = pd.read_csv(f's3://{self.bucket}/{self.key_read}')
        return df

    def write(self, df: DataFrame, folder: str) -> None:
        """
        Writes the DataFrame back to S3 as a CSV file.
        """
        df.to_csv(f's3://{self.bucket}/{folder}')
