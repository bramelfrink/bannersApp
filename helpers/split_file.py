"""
Splits the input files into smaller files.
"""
import os


def split(filename, delimiter=',', row_limit=200,
          output_path='out', keep_headers=True):
    """
    Splits a CSV file.
    """
    filehandler = open(filename, 'r')
    if 'clicks' in filename:
        dir = 'clicks'
    elif 'conversions' in filename:
        dir = 'conversions'
    else:
        dir = 'impressions'
    base_name_with_extension = filename.split('/')[-1]
    base_name = base_name_with_extension.split('.')[0]
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        dir,
        f'{base_name}_part_{current_piece}.csv'
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = next(reader)
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path,
                dir,
                f'{base_name}_part_{current_piece}.csv'
            )
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)


if __name__ == '__main__':
    split('csv/4/impressions_4.csv')
