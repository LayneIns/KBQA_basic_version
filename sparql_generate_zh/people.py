# -*- coding: utf-8 -*-
import re

from generate_query import generate_query_for_who_is, generate_query_for_director, generate_query_for_starring,\
	generate_query_for_author


def people_match(cut_res, s):
	if match_who_is(cut_res):
		return generate_query_for_who_is(cut_res)
	elif match_is_who(cut_res):
		return generate_query_for_who_is(cut_res)
	elif match_who_direct(s):
		return generate_query_for_director(s)
	elif match_who_starring(s):
		return generate_query_for_starring(s)
	elif match_who_author(s):
		return generate_query_for_author(s)
	else:
		return "Query not generated for this question"


def match_who_direct(s):
	pattern1 = re.compile(ur"谁导演了?(.+)")
	pattern2 = re.compile(ur"谁是.+的导演")
	if re.match(pattern1, s) or re.match(pattern2, s):
		return True
	return False


def match_who_starring(s):
	pattern1 = re.compile(ur"谁主演了?(.+)")
	pattern2 = re.compile(ur"谁是.+的主演")
	if re.match(pattern1, s) or re.match(pattern2, s):
		return True
	return False


def match_who_author(s):
	pattern1 = re.compile(ur"谁写了?(.+)")
	pattern2 = re.compile(ur"谁是.+的作者")
	pattern3 = re.compile(ur"(.+)是谁写的")
	if re.match(pattern1, s) or re.match(pattern2, s) or re.match(pattern3, s):
		return True
	return False


def match_is_who(cut_res):
	if len(cut_res) >= 3:
		r_match = (cut_res[2][0] == u"谁" and cut_res[2][1] == 'r')
		v_match = (cut_res[1][0] == u"是" and cut_res[1][1] == 'v')
		nr_match = (cut_res[0][1] == 'nr' or cut_res[0][1] == 'nrfg')
		if len(cut_res) > 3:
			x_match = (cut_res[3][1] == 'x')
		else:
			x_match = True

		if r_match and v_match and nr_match and x_match:
			return True
		else:
			return False
	else:
		return False


def match_who_is(cut_res):
	if len(cut_res) >= 3:
		r_match = (cut_res[0][0] == u"谁" and cut_res[0][1] == 'r')
		v_match = (cut_res[1][0] == u"是" and cut_res[1][1] == 'v')
		nr_match = (cut_res[2][1] == 'nr' or cut_res[2][0] == 'nrfg')
		if len(cut_res) > 3:
			x_match = (cut_res[3][1] == 'x')
		else:
			x_match = True

		if r_match and v_match and nr_match and x_match:
			return True
		else:
			return False
	else:
		return False