import camelot
# from tabula import read_pdf
# from tabulate import tabulate

file = r"ex_tables\foo.pdf"

tables = camelot.read_pdf(file)


print("Total tables extracted:", tables.n)