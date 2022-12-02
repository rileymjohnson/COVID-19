from selectolax.parser import HTMLParser
from unidecode import unidecode
from html import unescape
import regex as re


class Parser:
    @staticmethod
    def clean_and_extract_content(html):
        # All data extracted from html
        document_data = {}

        # Unescape HTML chars/symbols
        html = unescape(html.html)
        # Convert from unicode to ascii
        html = unidecode(html)
        # Convert back to html parser
        html = HTMLParser(html)

        # Get header & content (both within body)
        syndicates = html.css(':not(script).syndicate')

        # If not malformed
        if len(syndicates) > 1:
            header, content = syndicates[-2:]
        else:
            # Methods will work but won't find anything
            header = HTMLParser('')
            content = HTMLParser('')

        # Get header title
        title_tag = header.css_first('#content')
        if title_tag is not None:
            document_data['header_title'] = title_tag.text()
        else:
            document_data['header_title'] = None

        # Get page title
        title_tag = html.css_first('head title')
        if title_tag is not None:
            document_data['page_title'] = title_tag.text()
        else:
            document_data['page_title'] = None

        # Get header subtitle
        lead_tag = html.css_first('.lead')
        if lead_tag is not None:
            document_data['subtitle'] = lead_tag.text()
        else:
            document_data['subtitle'] = None

        # Get page metadata
        document_data['metadata'] = {}

        for meta_tag in html.css('meta'):
            if 'name' in meta_tag.attrs:
                key = meta_tag.attrs['name']
            elif 'property' in meta_tag.attrs:
                key = meta_tag.attrs['property']
            else:
                if 'charset' in meta_tag.attrs:
                    document_data['metadata']['charset'] = \
                        meta_tag.attrs['charset']
                continue

            if 'content' in meta_tag.attrs:
                document_data['metadata'][key] = \
                    meta_tag.attrs['content']

        # Remove "Top of Page" links
        top_of_page_links = content \
            .select('a') \
            .text_contains('Top of Page') \
            .matches

        for a_tag in top_of_page_links:
            a_tag.decompose()

        # Remove icons and their alt text
        for icon_tag in html.css('.sr-only, .fi'):
            icon_tag.decompose()

        # Convert img tags to their alts
        matches = content \
            .select('img') \
            .matches

        for img_tag in matches:
            img_alt = img_tag.attrs.get('alt')

            if img_alt:
                img_tag.replace_with(img_alt)

        # Remove 'View Larger' links
        matches = content \
            .select('a') \
            .text_contains('View Larger') \
            .matches

        for a_tag in matches:
            a_tag.decompose()

        # Remove 'Download Image' links
        matches = content \
            .select('a') \
            .text_contains('Download Image') \
            .matches

        for a_tag in matches:
            a_tag.decompose()

        # Unwrap button contents
        content.unwrap_tags(['button'])

        # Remove sup tags
        for sup_tag in content.css('sup'):
            sup_tag.decompose()

        # Determine title of document
        document_data['title'] = document_data.get('header_title',
                                    document_data.get('page_title'))

        # Add text content to document data
        document_text = content.text().strip()
        document_text = re.sub('[\t\r]', '', document_text)
        document_text = re.sub('\n+', '\n', document_text)
        document_data['text'] = document_text

        return content, document_data

    @classmethod
    def parse(cls, html, *, return_document_data=True):
        html, document_data = cls.clean_and_extract_content(html)

        if return_document_data:
            return html, document_data
        else:
            return html


from tempfile import mkstemp
import webbrowser
import os

def demo_html(html):
    # Opens selectolax object in webbrowser
    if hasattr(html, 'html'):
        html = html.html

    fd, path = mkstemp(suffix='.html')

    with os.fdopen(fd, 'wb') as f:
        f.write(html.encode('utf-8'))

    webbrowser.open(path)
