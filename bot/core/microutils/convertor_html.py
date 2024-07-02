import re

def apply_entity(entity, text):
    if entity.type == 'bold':
        return f'<b>{text}</b>'
    elif entity.type == 'italic':
        return f'<i>{text}</i>'
    elif entity.type == 'code':
        return f'<code>{text}</code>'
    elif entity.type == 'pre':
        return f'<pre>{text}</pre>'
    elif entity.type == 'underline':
        return f'<u>{text}</u>'
    elif entity.type == 'strikethrough':
        return f'<s>{text}</s>'
    elif entity.type == 'text_link':
        return f'<a href="{entity.url}">{text}</a>'
    elif entity.type == 'spoiler':
        return f'<tg-spoiler>{text}</tg-spoiler>'
    elif entity.type == 'custom_emoji':
        return f'<tg-emoji emoji-id="{entity.custom_emoji_id}">{text}</tg-emoji>'
    else:
        print(f"Unknown entity type: {entity.type}")
        return text

def apply_nested_entities(text, entities):
    if not entities:
        return text
    
    entity = entities[0]
    inner_text = apply_nested_entities(text, entities[1:])
    return apply_entity(entity, inner_text)

def apply_entities_to_text(text, entities):
    
    if not entities:
        print("No entities found")
        return text
    
    sorted_entities = sorted(entities, key=lambda e: (e.offset, -e.length))
    result = []
    last_offset = 0
    
    while sorted_entities:
        entity = sorted_entities.pop(0)
        if entity.offset > last_offset:
            result.append(text[last_offset:entity.offset])
        
        end_offset = entity.offset + entity.length
        overlapping_entities = [entity]
        while sorted_entities and sorted_entities[0].offset < end_offset:
            next_entity = sorted_entities.pop(0)
            if next_entity.offset + next_entity.length > end_offset:
                sorted_entities.insert(0, next_entity)
                break
            overlapping_entities.append(next_entity)
        
        entity_text = text[entity.offset:end_offset]
        formatted_text = apply_nested_entities(entity_text, overlapping_entities)
        result.append(formatted_text)
        
        last_offset = end_offset
    
    if last_offset < len(text):
        result.append(text[last_offset:])
    
    final_result = ''.join(result)
    final_result = re.sub(r'<i></i>', '', final_result)
    
    return final_result.strip()

def markdown_to_html(text):
    for pattern in [r'\|\|\*\*(.*?)\*\*\|\|', r'\*\*\|\|(.*?)\|\|\*\*', r'\|\|\*\*(.*?)\|\|\*\*', r'\*\*\|\|(.*?)\*\*\|\|']:
        text = re.sub(pattern, lambda m: f'<tg-spoiler><b>{m.group(1)}</b></tg-spoiler>', text)

    for pattern in [r'\|\|\*(.*?)\*\|\|', r'\*\|\|(.*?)\|\|\*', r'\|\|\*(.*?)\|\|\*', r'\*\|\|(.*?)\*\|\|']:
        text = re.sub(pattern, lambda m: f'<tg-spoiler><i>{m.group(1)}</i></tg-spoiler>', text)

    for pattern in [r'\|\|__(.*?)__\|\|', r'__\|\|(.*?)\|\|__', r'\|\|__(.*?)\|\|__', r'__\|\|(.*?)__\|\|']:
        text = re.sub(pattern, lambda m: f'<tg-spoiler><u>{m.group(1)}</u></tg-spoiler>', text)

    for pattern in [r'\|\|~~(.*?)~~\|\|', r'~~\|\|(.*?)\|\|~~', r'\|\|~~(.*?)\|\|~~', r'~~\|\|(.*?)~~\|\|']:
        text = re.sub(pattern, lambda m: f'<tg-spoiler><s>{m.group(1)}</s></tg-spoiler>', text)

    for pattern in [r'\|\|`(.*?)`\|\|', r'`\|\|(.*?)\|\|`', r'\|\|`(.*?)\|\|`', r'`\|\|(.*?)`\|\|']:
        text = re.sub(pattern, lambda m: f'<tg-spoiler><code>{m.group(1)}</code></tg-spoiler>', text)

    for pattern in [r'\*\*\*(.*?)\*\*\*', r'___(.*)___', r'\*\*_(.*?)_\*\*', r'__\*(.*?)\*__', r'_\*\*(.*?)\*\*_', r'\*__(.*)__\*', r'_\*\*\*(.*?)\*\*\*_', r'\*\*\*_(.*?)_\*\*\*', r'__\*\*(.*?)\*\*__', r'\*\*__(.*?)__\*\*']:
        text = re.sub(pattern, lambda m: f'<b><i>{m.group(1)}</i></b>', text)

    conversions = [
        (r'\|\|(.*?)\|\|', r'<tg-spoiler>\1</tg-spoiler>'),
        (r'\*\*(.*?)\*\*', r'<b>\1</b>'),
        (r'\*(.*?)\*', r'<i>\1</i>'),
        (r'_(.*?)_', r'<i>\1</i>'),
        (r'`(.*?)`', r'<code>\1</code>'),
        (r'```(.*?)```', r'<pre><code>\1</code></pre>', re.DOTALL),
        (r'`{3}(\w+)\n(.*?)\n`{3}', r'<pre><code class="\1">\2</code></pre>', re.DOTALL),
        (r'__(.*?)__', r'<u>\1</u>'),
        (r'~~(.*?)~~', r'<s>\1</s>'),
        (r'~(.*?)~', r'<s>\1</s>'),
        (r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>'),
        (r'<(https?://[^\s>]+)>', r'<a href="\1">\1</a>'),
        (r'\*(\*\*.*?\*\*)\*', r'<i><b>\1</b></i>'),
        (r'_(\*\*.*?\*\*)_', r'<i><b>\1</b></i>'),
        (r'\*\*_(.*?)_\*\*', r'<b><i>\1</i></b>'),
        (r'__\*(.*?)\*__', r'<u><i>\1</i></u>'),
        (r'\|\|\|\|(.*?)\|\|\|\|', r'<tg-spoiler><tg-spoiler>\1</tg-spoiler></tg-spoiler>'),
        (r'^&gt; (.+)$', r'<blockquote>\1</blockquote>', re.MULTILINE),
        (r'^\s*[-*+]\s(.+)$', r'<li>\1</li>', re.MULTILINE),
    ]

    for pattern, replacement, *flags in conversions:
        text = re.sub(pattern, replacement, text, flags=flags[0] if flags else 0)
        
    text = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', text, flags=re.DOTALL)
    text = re.sub(r'<i></i>', '', text)

    return text
