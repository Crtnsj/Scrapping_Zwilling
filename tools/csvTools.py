import polars as pl
import re


def concatCSV(csvList):
    finalCSV = pl.read_csv(csvList[0]).with_columns(pl.col(pl.Int64).cast(pl.Utf8))

    for i in range(1, len(csvList), 1):
        df = pl.read_csv(csvList[i]).with_columns(pl.col(pl.Int64).cast(pl.Utf8))
        finalCSV = pl.concat([df, finalCSV])

    return finalCSV


def addRefColumn(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.col("url")
        .map_elements(
            lambda url: (
                re.search(r"/([^/]+)\.html$", url).group(1)
                if re.search(r"/([^/]+)\.html$", url)
                else None
            )
        )
        .alias("REF")
    )


# df = pl.read_csv("../dataframes/data.csv")

# dataWithRef = addRefColumn(df)
# dataWithRef.write_csv("../dataframes/dataWithRef.csv")
