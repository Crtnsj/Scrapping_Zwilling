import xml.etree.ElementTree as ET
import polars as pl
import re
import requests


def getSitemap(url, output_file):
    """
    Downloads a sitemap from a given URL and saves it to a file.

    Args:
    url: str
    The URL of the sitemap
    output_file: str
    The path to save the sitemap file
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"Sitemap downloaded successfully and saved to {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download sitemap: {e}")


def getUrlsFromXml(sitemap_file):
    """
    Extracts URLs and references from an XML sitemap file.
    And returns a polars Dataframe

    Args:
    sitemap_file: str
    The path to the XML sitemap file

    Returns:
    pl.DataFrame

    """
    tree = ET.parse(sitemap_file)
    root = tree.getroot()
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text for loc in root.findall("ns:url/ns:loc", namespace)]

    refs = [
        (
            re.search(r"/([^/]+)\.html$", url).group(1)
            if re.search(r"/([^/]+)\.html$", url)
            else None
        )
        for url in urls
    ]

    df = pl.DataFrame(
        {
            "url": urls,
            "ref": refs,
        }
    )

    return df
