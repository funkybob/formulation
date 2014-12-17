
from contextlib import contextmanager
from copy import copy

from django import template
try:
    from django.forms.utils import flatatt
except ImportError:  # Django 1.5 compatibility
    from django.forms.util import flatatt
from django.template.loader import get_template
from django.template.loader_tags import (
    BlockNode, ExtendsNode, BlockContext, BLOCK_CONTEXT_KEY,
)
from django.utils import six
from django.utils.encoding import force_text

register = template.Library()


def resolve_blocks(template, context):
    '''Get all the blocks from this template, accounting for 'extends' tags'''
    try:
        blocks = context.render_context[BLOCK_CONTEXT_KEY]
    except KeyError:
        blocks = context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()

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
        resolve_blocks(parent_template, context)

    return blocks


@contextmanager
def extra_context(context, extra):
    '''Temporarily add some context, and clean up after ourselves.'''
    context.update(extra)
    yield
    context.pop()


@register.tag
def form(parser, token):
    '''Prepare to render a Form, using the specified template.

    {% form "template.form" [form] %}
        {% field "blockname" form.somefield ..... %}
        ...
    {% endform %}
    '''
    bits = token.split_contents()
    tag_name = bits.pop(0)  # Remove the tag name
    try:
        tmpl_name = parser.compile_filter(bits.pop(0))
    except IndexError:
        raise template.TemplateSyntaxError("%r tag takes at least 1 argument: "
                                           "the widget template" % tag_name)

    try:
        form = parser.compile_filter(bits.pop(0))
    except IndexError:
        form = None

    nodelist = parser.parse(('endform',))
    parser.delete_first_token()

    return FormNode(tmpl_name, nodelist, form)


class FormNode(template.Node):
    def __init__(self, tmpl_name, nodelist, form):
        self.tmpl_name = tmpl_name
        self.nodelist = nodelist
        self.form = form

    def render(self, context):
        # Resolve our arguments
        tmpl_name = self.tmpl_name.resolve(context)

        form = self.form
        if form is not None:
            form = form.resolve(context)

        safe_context = copy(context)
        # Since render_context is derived from BaseContext, a simple copy will
        # wind up with the same stack of dicts.
        safe_context.render_context = safe_context.render_context.new({
            BLOCK_CONTEXT_KEY: BlockContext(),
        })

        extra = {
            'formulation': resolve_blocks(tmpl_name, safe_context),
            'formulation-form': form,
        }

        # Render our children
        with extra_context(safe_context, extra):
            return self.nodelist.render(safe_context)


@register.simple_tag(takes_context=True)
def field(context, field, widget=None, **kwargs):
    if isinstance(field, six.string_types):
        field = context['formulation-form'][field]

    field_data = {
        'form_field': field,
        'id': field.auto_id,
        'widget_type': field.field.widget.__class__.__name__,
        'field_type': field.field.__class__.__name__,
    }

    for attr in ('css_classes', 'errors', 'field', 'form', 'help_text',
                 'html_name', 'id_for_label', 'label', 'name', 'value',):
        field_data[attr] = getattr(field, attr)

    for attr in ('choices', 'widget', 'required'):
        field_data[attr] = getattr(field.field, attr, None)

    if field_data['choices']:
        field_data['display'] = dict(field.field.choices).get(field.value, '')
        field_data['choices'] = [
            (force_text(k), v)
            for k, v in field_data['choices']
        ]
        # Normalize the value [django.forms.widgets.Select.render_options]
        value = field_data['value']()
        field_data['value'] = [force_text(v) for v in value] \
                              if isinstance(value, (list, tuple)) \
                              else force_text(value)

    # Allow supplied values to override field data
    field_data.update(kwargs)

    if widget is None:
        widgets = auto_widget(field)
    else:
        widgets = [widget]
    for name in widgets:
        block = context['formulation'].get_block(name)
        if block is not None:
            break

    if block is None:
        raise template.TemplateSyntaxError(
            "No widget for field: %s (%r) [Tried: %s]" % (
                field.name,
                field.field,
                widgets
            )
        )

    field_data['block'] = block
    with extra_context(context, field_data):
        return block.render(context)


@register.simple_tag(takes_context=True)
def use(context, widget, **kwargs):
    kwargs['block'] = block = context['formulation'].get_block(widget)
    with extra_context(context, kwargs):
        return block.render(context)


@register.filter
def flat_attrs(attrs):
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
