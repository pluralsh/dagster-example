import requests
import pandas as pd

from dagster import asset, get_dagster_logger, Output, MetadataValue
# add an import to the Output and MetadataValue classes from the dagster library

import matplotlib.pyplot as plt
import base64
from io import BytesIO
from wordcloud import STOPWORDS, WordCloud

@asset # add the asset decorator to tell Dagster this is an asset
def topstory_ids():
    """This is a sample documentation for topstory_ids"""
    newstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    top_new_story_ids = requests.get(newstories_url).json()[:100]
    return top_new_story_ids


@asset
def topstories(topstory_ids):
    logger = get_dagster_logger()

    results = []
    for item_id in topstory_ids:
        item = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        ).json()
        results.append(item)

        if len(results) % 20 == 0:
            logger.info(f"Got {len(results)} items so far.")

    df = pd.DataFrame(results)

    return Output(  # The return value is updated to wrap it in `Output` class
        value=df,   # The original df is passed in with the `value` parameter
        metadata={
            "num_records": len(df), # Metadata can be any key-value pair
            "preview": MetadataValue.md(df.head().to_markdown()),
            # The `MetadataValue` class has useful static methods to build Metadata
        }
    )

# adding the word cloud asset
@asset
def topstories_word_cloud(topstories):
    stopwords = set(STOPWORDS)
    stopwords.update(["Ask", "Show", "HN", "S"])
    titles_text = " ".join([str(item) for item in topstories["title"]])
    titles_cloud = WordCloud(stopwords=stopwords, background_color="white").generate(titles_text)

    # Generate the word cloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(titles_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)

    # Since we're saving the asset, this converts the word cloud into an image
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    image_data = base64.b64encode(buffer.getvalue())

    # Addition: Turn the image into Markdown to embed it into the metadata
    md_content = f"![img](data:image/png;base64,{image_data.decode()})"

    # Addition: Attach the Markdown content as metadata to the asset
    return Output(value=image_data, metadata={
        "plot": MetadataValue.md(md_content)
    })
