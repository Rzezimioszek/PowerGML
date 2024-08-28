import pandas as pd

def save_xlsx(bdict, path):
    path = path + '.xlsx'

    try:
        with pd.ExcelWriter(path) as writer:
            for key, val in bdict.items():
                df = pd.DataFrame(val)
                df.to_excel(writer, sheet_name=key, header=True, index=False)

            df = None

    except PermissionError:
        print("Nie da się zapisać")

if __name__ == "__main__":
    ...