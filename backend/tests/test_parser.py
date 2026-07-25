from app.parser.parse import parse_html_document


SAMPLE_HTML = """
<html>
  <head>
    <title>Example Title</title>
    <meta name="description" content="Example description" />
  </head>
  <body>
    <h1>Heading One</h1>
    <h1>Heading Two</h1>
    <img src="/a.png" alt="" />
    <img src="/b.png" alt="Accessible" />
    <p>Visible text for the page</p>
    <script>var hidden = 1;</script>
    <style>.hidden { display: none; }</style>
  </body>
</html>
"""


def test_parse_html_document_returns_expected_fields():
    report = parse_html_document(SAMPLE_HTML)

    assert report["title"] == "Example Title"
    assert report["metaDescription"] == "Example description"
    assert report["h1Count"] == 2
    assert report["imagesMissingAlt"] == 1
    assert report["totalImages"] == 2
    assert report["approxWordCount"] >= 4


def test_parse_html_document_handles_missing_metadata_and_images():
    report = parse_html_document("<html><body><p>Only visible text here.</p></body></html>")

    assert report["title"] is None
    assert report["metaDescription"] is None
    assert report["h1Count"] == 0
    assert report["imagesMissingAlt"] == 0
    assert report["totalImages"] == 0
    assert report["approxWordCount"] == 4
