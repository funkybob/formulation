
from django import template
from django.template.base import token_kwargs
from django.template.loader import get_template
from django.template.loader_tags import BlockNode, ExtendsNode, BlockContext

register = template.Library()

def resolve_blocks(template, context, blocks=None):
    '''Get all the blocks from this template, accounting for 'extends' tags'''
    if blocks is None:
        blocks = BlockContext()

    # If it's just the name, resolve into template
    if isinstance(template, basestring):
        template = get_template(template)

    # Add this templates blocks as the first
    local_blocks = dict(
        (block.name, block)
        for block in template.nodelist.get_nodes_by_type(BlockNode)
    )
    blocks.add_blocks(local_blocks)

    # Do we extend a parent template?
    extends = template.nodelist.get_nodes_by_type(ExtendsNode)
    if extends:
        # Can only have one extends in a template
        extends_node = extends[0]

        # Get the parent, and recurse
        parent_template = extends_node.get_parent(context)
        resolve_blocks(parent_template, context, blocks)

    return blocks


@register.tag
def form(parser, token):
    '''Open a context providing blocks from the named sniplate'''
    bits = token.split_contents()
    tag_name = bits.pop(0) # Remove the tag name
    try:
        tmpl_name = parser.compile_filter(bits.pop(0))
    except IndexError:
        raise template.TemplateSyntaxError("%r tag takes at least 1 argument: the widget template" % tag_name)

    kwargs = token_kwargs(bits, parser)

    nodelist = parser.parse(('endform',))
    parser.delete_first_token()

    return FormNode(tmpl_name, nodelist, kwargs)


class FormNode(template.Node):
    def __init__(self, tmpl_name, nodelist, kwargs):
        self.tmpl_name = tmpl_name
        self.nodelist= nodelist
        self.kwargs = kwargs

    def render(self, context):
        # Resolve our arguments
        tmpl_name = self.tmpl_name.resolve(context)
        kwargs = dict(
            (key, val.resolve(context))
            for key, val in self.kwargs.items()
        )

        # Grab the template snippets
        kwargs['formulation'] = resolve_blocks(tmpl_name, context)

        # Render our children
        context.update(options)
        output = self.nodelist.render(context)
        context.pop()

        return output


@register.simple_tag(takes_context=True)
def field(context, field, widget, **kwargs):
    kwargs['field'] = field
    context.update(options)
    output = context['formulation'].get_block(widget).render(context)
    context.pop()

    return output


@register.simple_tag(takes_context=True)
def use(context, widget, **kwargs):
    context.push(kwargs)
    output = context['formulation'].get_block(widget).render(context)
    context.pop()

    return output

