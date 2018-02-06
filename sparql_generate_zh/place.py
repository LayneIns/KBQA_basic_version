# coding: utf-8
import re

from generate_query import generate_query_for_capital, generate_query_for_from


def place_match(cut_res, s):
    if match_where_capital_is(s):
        return generate_query_for_capital(s)
    elif match_where_from(s):
        return generate_query_for_from(s)
    else:
        return "Query not generated for this question"


def match_where_from(s):
    pattern1 = re.compile(ur"(.+)来自哪里")
    if re.match(pattern1, s):
        return True
    return False


def match_where_capital_is(s):
    pattern1 = re.compile(ur"(.+)的首都(在|是)哪里")
    if re.match(pattern1, s):
        return True
    return False


