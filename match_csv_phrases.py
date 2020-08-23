import csv
import sys
import re
import logging


def read_input_csv(filename, **kwargs):
    filename = filename + ".csv" if ".csv" not in filename else filename

    with open(filename) as f:
        file_lod = [{k:v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)] # LOD

    print(f"Length of input CSV is: {len(file_lod)}")

    if kwargs.get("columns") and any(x for x in kwargs["columns"] if x not in file_lod[0].keys()):
        sys.exit(f"Exiting. Your CSV needs to have these columns: {kwargs['columns']}")

    if kwargs.get("start_row"):
        file_lod = file_lod[kwargs["start_row"]:]

    if kwargs.get("url_column"):
        file_lol = [x[kwargs["url_column"]] for x in file_lod if is_url(x[kwargs["url_column"]])] # throw out empty cells
        print(f"Length of input CSV after removing non-URL rows and accounting for start_at is: {len(file_lol)}")
        return file_lol

    print(f"Length of input CSV after accounting for start_at is: {len(file_lod)}")
    return file_lod


def write_output_csv(filename, start_row, output_lod):
    filename = filename + ".csv" if ".csv" not in filename else filename

    with open(f"Output {start_row} - {filename}", 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, output_lod[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(output_lod)
    print("Write to csv was successful\n")


###########################################################################################################


def match_substring_categories(row, text_col, phrases_lod, phrases_col, phrases_cat_col, pattern):
    matched_phrases_list = [x.groups()[1] for x in re.finditer(pattern, row[text_col])]
    matched_phrases_lod = [x for x in phrases_lod if x[phrases_col] in matched_phrases_list]
    row["Tags"] = ", ".join([x[phrases_col] for x in matched_phrases_lod if x[phrases_col]])
    row["Tag_Types"] = ", ".join([x[phrases_cat_col] for x in matched_phrases_lod if x[phrases_cat_col]])

    return row


############################################################################################################


if __name__ == "__main__":

    csv.field_size_limit(100000000)

    data_filename = "Combined Post Data 8.22.csv"
    data_text_col = "text"
    start_row = 11000

    phrases_filename = "SS_Tag_Products_With_Cats_8.22.csv"
    phrases_col = "product"
    phrases_category_col = "Unique tags"

    input_lod = read_input_csv(
        data_filename,
        start_row=start_row,
        columns=[data_text_col]
    )
    substring_lookup_lod = read_input_csv(phrases_filename, columns=[phrases_col, phrases_category_col])

    substring_list = list(set([re.escape(x[phrases_col]) for x in substring_lookup_lod]))
    pattern = re.compile("(\s)(" + '|'.join(substring_list) + ")(,|\.|\s|;)")

    output_lod = []
    for n, row in enumerate(input_lod):
        row = match_substring_categories(row, "text", substring_lookup_lod, phrases_col, phrases_category_col, pattern)
        output_lod.append(row)
        if n % 100 == 0:
            print(n)
        if n % 1000 == 0:
            write_output_csv("Output " + filename, start_row, output_lod)



############################################################################################################