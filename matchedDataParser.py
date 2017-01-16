import csv

input_file = './csv/matched_data_orig.csv'
output_file = './csv/transformed_matched_data.csv'

with open(input_file,
          mode='rt',
          errors='strict',
          encoding='utf-8') as orig_data:
    reader = csv.reader(orig_data,
                        delimiter=',',
                        quoting=csv.QUOTE_NONE,
                        strict=True)
    headerRow = next(reader)
    print(headerRow)

