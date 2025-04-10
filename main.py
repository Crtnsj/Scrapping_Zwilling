import tools.sitemapTools as st
import tools.csvTools as ct
import tools.scrapper as sc
import polars as pl

"""
Prepocessing the data
    # sitemap_url = "https://www.zwilling.com/fr/sitemap_0-product.xml"
    # sitemap_path = "./xmls/sitemap.xml"
    # st.getSitemap(sitemap_url, sitemap_path)
    # urls = st.getUrlsFromXml(sitemap_path)
    # urls.write_csv("./dataframes/urls.csv")
    # concat_csv = ct.concatCSV(
    #     [
    #         "./PricesLists/Ballarini.csv",
    #         "./PricesLists/Demeyre.csv",
    #         "./PricesLists/MIYABI.csv",
    #         "./PricesLists/ZWILLING.csv",
    #     ]
    # )
    # concat_csv.write_csv("./dataframes/prices.csv")
"""

if __name__ == "__main__":
    urls = pl.read_csv(
        "./dataframes/urls_for_test.csv", schema_overrides={"ref": pl.Utf8}
    )
    priceList = pl.read_csv(
        "./dataframes/Prices.csv", schema_overrides={"REF": pl.Utf8, "PCB": pl.Utf8}
    )
    data = sc.get_data(
        urls,
        priceList,
    )
    data.write_csv("./dataframes/test.csv")
