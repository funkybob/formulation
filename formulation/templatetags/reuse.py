
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def reuse(context, block_list, **kwargs):
    '''
    Allow reuse of a block within a template.

    {% reuse '_myblock' foo=bar %}
    {% reuse list_of_block_names .... %}
    '''
    # This must be inline to avoid circular import
    from django.template.loader_tags import BLOCK_CONTEXT_KEY
    block_context = context.render_context[BLOCK_CONTEXT_KEY]

    if not isinstance(block_list, list):
        block_list = [block_list]

    for name in block_list:
        block = block_context.get_block(name)
        if block is not None:
            break

    if block is None:
        return ''

    # Replace this with "with context.update()" when 1.7 lands
    context.update(kwargs)
    content = block.render(context)
    context.pop()
    return content
