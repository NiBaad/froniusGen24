import pandas as pd
import os
import pathlib

CONFIG = "{ address=40265, name=\"DCA_SF\", type=\"INT16\" }"

# acc16 uint16
# acc32 uint32
# acc64 uint64
# sunssf int16
# enum16 uint16

def main():
    main_path = os.path.dirname(os.path.realpath(__file__))
    main_files = os.listdir(main_path)
    excel_file_path = None
    
    for file in main_files:
        if ".xlsx" in file:
            excel_file_path = pathlib.Path(main_path)
            excel_file_path = excel_file_path / file
            break
    else:
        exit(255)
    
    df = pd.read_excel(excel_file_path, skiprows=2, index_col=None)
    df.columns = [c.replace("\n", " ") for c in df.columns]
    df.replace(r'\n',' ', regex=True, inplace=True) 
    df.dropna(how='all', inplace=True)
    df.drop_duplicates(keep=False, inplace=True)
    #df.dropna(subset="Units", inplace=True)
    
    range_filter = df["Range of values"].str.contains("not supported")
    range_filter.fillna(False, inplace=True)
    print(range_filter)
    df = df[~range_filter]
    
    reg_filter = df["Units"].str.contains("Registers").fillna(False)
    df = df[~reg_filter]
    
    per_filter = df["Units"].str.contains("%").fillna(False)
    df.loc[per_filter, "Units"] = "%"
    
    for i in [16, 32, 64]:
        per_filter = df["Type"].str.contains(f"acc{i}")
        df.loc[per_filter, "Type"] = f"uint{i}"

    print (df[["Start", "Size", "Name", "Type", "Units", "Scale Factor"]])
    
    #print(df.head())
    #df = df.reset_index()
    #for index, row in df.iterrows():
    #   print(f"{{ address={row['Start']}, name=\"{row['Name']}\", type=\"{str(row['Type']).upper()}}}\"")
    
    mindf = df[["Start", "Name", "Type", "Units", "Scale Factor"]]
    mindf.to_csv('out.csv', index=False)  

if __name__ == "__main__":
    main()