import re

def update_heading(markdown):
    file_content = markdown.split('\n')
    markdown = ''
    code = False
    for line in file_content:
        if not code:
            if line.startswith('```'):
                code = True
            elif line.startswith('#') and line.count('#')<=5:
                heading_number = line.count('#') + 1
                line = '#' * heading_number + ' ' + line.replace('#', '')
        elif line.startswith('```') and code:
            code = True
        markdown += line + '\n'
    return markdown

def strip_comments(markdown):
    file_content = markdown.split('\n')
    markdown = ''
    for line in file_content:
        if not re.search(r'%%(.*)%%', line) or not line.startswith('%%') or not line.endswith('%%'):
            markdown += line + '\n'
    markdown = re.sub(r'%%(.*)%%', '', markdown, flags=re.DOTALL)
    return markdown

def fix_tags(metadata):
    tags = metadata.get('tags', None) or metadata.get('tag', None)
    if tags and isinstance(tags, str):
        tags = tags.split('/')
        tags = [tag.strip() for tag in tags]
        metadata['tags'] = tags
    return metadata

def on_page_markdown(markdown, files, page, **kwargs):
    markdown = strip_comments(markdown)
    markdown = update_heading(markdown)
    metadata = fix_tags(page.meta)
    page.meta = metadata
    return markdown