
from contextlib import contextmanager

from django import template
try:
    from django.forms.utils import flatatt
except ImportError: # Django 1.5 compatibility
    from django.forms.util import flatatt
from django.template.loader import get_template
from django.template.loader_tags import BlockNode, ExtendsNode, BlockContext
from django.utils import six

register = template.Library()

def resolve_blocks(template, context, blocks=None):
    '''Get all the blocks from this template, accounting for 'extends' tags'''
    if blocks is None:
        blocks = BlockContext()

    # If it's just the name, resolve into template
    if isinstance(template, six.string_types):
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


@contextmanager
def extra_context(context, extra):
    '''Temporarily add some context, and clean up after ourselves.'''
    context.update(extra)
    yield
    context.pop()


@register.simple_tag(takes_context=True)
def load_widgets(context, template_name, var=None):
    '''Load a widget set'''
    nodelist = resolve_blocks(template_name, context)
    if var is None:
        var = 'default'
    context.setdefault('widgets', {})[var] = nodelist


@register.simple_tag(takes_context=True)
def widget(context, name, using=None, **kwargs):
    '''Render a widget'''
    if using is None:
        using = 'default'

    with extra_context(context, kwargs) as context:
        return context['widgets'][using].render(context)


@register.simple_tag(takes_context=True)
def field(context, field, widget=None, using=None, form=None, **kwargs):
    '''Render a field'''
    if using is None:
        using = 'default'

    if isinstance(field, six.string_types) and form is not None:
        field = form[field]

    field_data = {
        'form_field': field,
        'id': field.auto_id,
    }

    for attr in ('css_classes', 'errors', 'field', 'form', 'help_text',
                'html_name', 'id_for_label', 'label', 'name', 'value',):
        field_data[attr] = getattr(field, attr)

    for attr in ('choices', 'widget', 'required'):
        field_data[attr] = getattr(field.field, attr, None)

    kwargs.update(field_data)

    nodelist = context['widgets'][using]

    if widget is None:
        for name in auto_widget(field):
            block = nodelist.get_block(name)
            if block is not None:
                break
    else:
        block = nodelist.get_block(widget)

    if block is None:
        raise template.TemplateSyntaxError("Could not find widget for field: %r" % field)

    kwargs['block'] = block
    with extra_context(context, kwargs):
        return block.render(context)


@register.filter
def flatattrs(attrs):
    '''Helpful wrapper'''
    return flatatt(attrs)

@register.filter
def auto_widget(field):
    '''Return a list of widget names for the provided field.'''
    # Auto-detect
    info = {
        'widget': field.field.widget.__class__.__name__,
        'field': field.field.__class__.__name__,
        'name': field.name,
    }

    return [
        fmt.format(**info)
        for fmt in (
            '{field}_{widget}_{name}',
            '{field}_{name}',
            '{widget}_{name}',
            '{field}_{widget}',
            '{name}',
            '{widget}',
            '{field}',
        )
    ]

