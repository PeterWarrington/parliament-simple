import json
import os
import sys
import requests
import datetime
from google import genai
from google.genai import types
import pathlib

PREAMBLE = """
You are working for a website called "Parliament Simple"
which 'presents the most notable speeches of the House of Commons and the House of Lords every week, without spin, and without the boring bits.'.

Articles are almost entirely verbatim, but structured to highlight the key, most interesting points of debates.

Parliament Simple's motto is 'Know the debates of our time.'
"""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate-posts.py debate.md")
        sys.exit(1)

    debate_md = sys.argv[1]

    with open(debate_md, 'r') as f:
        debate_article = f.read()

    prompt = f"""
    Use the attached template SVGs to generate Instagram style posts which include the
    details of the article and the 'key quotes' section of the debate article.

    The debate article is as follows:

    ```
    {debate_article}
    ```

    Output the SVGs for all pages in the following repeated format:
    ```
    [SVG CONTENT]
    __NEW_PAGE__
    ```

    This should be the ENTIRETY of your response - do not include any other text. Do not enclose with ```json or any other code block markers.
    """

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=f"""
        PREAMBLE:
        {PREAMBLE}

        ATTACHED TEMPLATE FILES:
        cover.svg:
        ```
        {open("post-template/cover.svg").read()}
        ```
        middle.svg:
        ```
        {open("post-template/middle.svg").read()}
        ```
        end.svg:
        ```
        {open("post-template/end.svg").read()}
        ```

        PROMPT:
        {prompt}
        """,
    )

    output = response.text

    print(output)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # write svgs to .post_outputs/[timestamp]/[page_number].svg
    output_dir = f".post_outputs/{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    pages = output.split("__NEW_PAGE__")
    for i, page in enumerate(pages):
        page = page.strip()
        output_file_name = f"{output_dir}/{i+1}.svg"
        with open(output_file_name, 'w') as f:
            f.write(page)