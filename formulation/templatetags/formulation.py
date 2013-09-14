
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


class ContextDict(dict):
    '''Back-port of the ContextDict from Django 1.7'''
    def __init__(self, context, *args, **kwargs):
        super(ContextDict, self).__init__(*args, **kwargs)

        context.dicts.append(self)
        self.context = context

    def __enter__(self):
        self.context.update(self)
        return self.context

    def __exit__(self, *args, **kwargs):
        self.context.pop()


@register.tag
def form(parser, token):
    '''Prepare to render a Form, using the specified template.

    {% form "template.form" %}
        {% field "blockname" form.somefield ..... %}
        ...
    {% endform %}
    '''
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
        self.nodelist = nodelist
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
        with ContextDict(context, kwargs) as context:
            return self.nodelist.render(context)

def _auto_widget(field, context):
    # Auto-detect
    info = {
        'widget': field.field.widget.__class__.__name__,
        'field': field.field.__class__.__name__,
        'name': field.name,
    }

    for pattern in (
            '{field}_{widget}_{name}',
            '{field}_{name}',
            '{widget}_{name}',
            '{field}_{widget}',
            '{name}',
            '{widget}',
            '{field}',
        ):
        block = context['formulation'].get_block(
            pattern.format(info)
        )
        if block is not None:
            return block
    raise TemplateSyntaxError("Could not find widget for field: %r" % field)
    

@register.simple_tag(takes_context=True)
def field(context, field, widget=None, **kwargs):
    field_data = {
        'form_field': field,
        'id': field.auto_id,
    }
    for attr in ('css_classes', 'errors', 'field', 'form',
            'help_text', 'id_for_label', 'label', 'name', 'html_name',
            'value',):
        field_data[attr] = getattr(field, attr)
    for attr in ('choices', 'widget', 'required'):
        field_data[attr] = getattr(field.field, attr, None)
    kwargs.update(field_data)
    if widget is None:
        widget = _auto_widget(field, context)
    kwargs['block'] = block = context['formulation'].get_block(widget)
    with ContextDict(context, kwargs) as context:
        return block.render(context)


@register.simple_tag(takes_context=True)
def use(context, widget, **kwargs):
    kwargs['block'] = block = context['formulation'].get_block(widget)
    with ContextDict(context, kwargs) as context:
        return block.render(context)

