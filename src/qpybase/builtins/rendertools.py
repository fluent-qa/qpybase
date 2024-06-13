#!/usr/bin/env python
"""
render by jinja2 template engine
"""
import json
from typing import Callable

from jinja2 import Template

from . import randomtools
from .datetools import get_date_by_timedelta
from .randomtools import faker
from .randomtools import random_str

__all__ = [
    "render_template",
    "render_without_context",
    "render_to_dict",
    "register_render_func"
]

render_func = {
    "get_date_by_timedelta": get_date_by_timedelta,
    "faker": faker,
    "random_str": random_str,
    "randoms": randomtools
}


def register_render_func(render_func_name: str, func: Callable):
    render_func[render_func_name] = func


def render_template(temp_str, context):
    template = Template(temp_str)
    template.globals.update(render_func)
    return template.render(context)


def render_without_context(temp_str, default_return_str="N"):

    if temp_str is None:
        return default_return_str
    # print(temp_str)
    return render_template(temp_str, {})


def render_to_dict(dict_or_json, context):
    template = Template(json.dumps(dict_or_json))
    template.globals.update(render_func)
    filled_str = template.render(context)
    return json.loads(filled_str, encoding="utf-8")
