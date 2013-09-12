
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def reuse(context, block_name, **kwargs):
    '''
    Allow reuse of a block within a template.

    {% resuse '_myblock' foo=bar %}
    '''
    # This must be inline to avoid circular import
    from django.template.loader_tags import BLOCK_CONTEXT_KEY
    block = context.render_context[BLOCK_CONTEXT_KEY].get_block(block_name)
    if block is None:
        return ''
    # Replace this with "with context.update()" when 1.7 lands
    context.update(kwargs)
    content = block.render(context)
    context.pop()
    return content

