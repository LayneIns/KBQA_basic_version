# -*- coding: utf-8 -*-
import re


def add_prefix():
	prefix = u"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n\
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n\
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n\
PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n\
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>\n\
PREFIX quepy: <http://www.machinalis.com/quepy#>\n\
PREFIX dbpedia: <http://dbpedia.org/ontology/>\n\
PREFIX dbpprop: <http://zh.dbpedia.org/property/>\n\
PREFIX dbpedia-owl: <http://zh.dbpedia.org/ontology/>\n\n"
	return prefix


def generate_query_for_who_is(cut_res):
	prefix = add_prefix()

	if cut_res[2][1] == 'nr' or cut_res[2][1] == 'nrfg':
		name = cut_res[2][0]
	elif cut_res[0][1] == 'nr' or cut_res[0][1] == 'nrfg':
		name = cut_res[0][0]

	body = u"SELECT DISTINCT ?answer ?name ?comment ?birthplace_name1 ?birthplace_name2 ?birthplace_name3 ?birthplace_name4" \
		   u" ?birthday1 ?birthday2 ?birthday3 ?university_name ?picture FROM <http://zh.dbpedia.org> WHERE {\n"

	body += u"  ?x0 rdfs:comment ?answer.\n" \
			u"  FILTER (?x0=<http://zh.dbpedia.org/resource/" + name + u">)\n" \
			u"  ?x0 rdfs:comment ?comment.\n" \
			u"  ?x0 rdfs:label ?name.\n" \
			u"  OPTIONAL {?x0 dbpprop:出生地點 ?birthplace_name1.}\n" \
			u"  OPTIONAL {?x0 dbpprop:出生地点 ?birthplace_name2.}\n" \
			u"  OPTIONAL {?x0 dbpprop:出生地 ?birthplace_name3.}\n" \
			u"  OPTIONAL {?x0 dbpprop:birthPlace ?birthplace_name4.}\n" \
			u"  OPTIONAL {?x0 dbpprop:出生日期 ?birthday1.}\n" \
			u"  OPTIONAL {?x0 dbpprop:birthdate ?birthday2.}\n" \
			u"  OPTIONAL {?x0 dbpprop:birthDate ?birthday3.}\n" \
			u"  OPTIONAL {?x0 dbpprop:母校 ?university_link.\n" \
			u"            ?university_link rdfs:label ?university_name}\n" \
			u"  OPTIONAL {?x0 foaf:depiction ?picture.}\n" \
			u"}\n"

	body_short = u"SELECT DISTINCT ?answer  FROM <http://zh.dbpedia.org> WHERE {\n"
	body_short += u"  ?x0 rdfs:comment ?answer.\n" \
				u"  FILTER (?x0=<http://zh.dbpedia.org/resource/" + name + u">)\n" \
				u"}\n\n"

	return prefix + body_short + "###\n\n" + prefix + body


def generate_query_for_director(s):
	pattern1 = re.compile(ur"谁导演了?(.+)")
	pattern2 = re.compile(ur"谁是(.+)的导演")
	name = re.findall(pattern1, s)
	if len(name) == 0:
		name = name = re.findall(pattern2, s)
	if len(name) != 0:
		name = name[0]

	prefix = add_prefix()

	body = u"SELECT DISTINCT ?answer ?name ?comment ?birthplace_name1 ?birthplace_name2 ?birthplace_name3 ?birthplace_name4" \
		   u" ?birthday1 ?birthday2 ?birthday3 ?university_name ?picture FROM <http://zh.dbpedia.org> WHERE {\n"

	body += u"  ?x1 dbpprop:director ?x0.\n" \
			u"  ?x0 rdfs:label ?answer.\n" \
			u"  FILTER (?x1=<http://zh.dbpedia.org/resource/" + name + u">)\n" \
			u"  OPTIONAL {?x0 rdfs:comment ?comment.}\n" \
			u"  ?x0 rdfs:label ?name.\n" \
			u"  OPTIONAL {?x0 dbpprop:出生地點 ?birthplace_name1.}\n" \
			u"  OPTIONAL {?x0 dbpprop:出生地点 ?birthplace_name2.}\n" \
			u"  OPTIONAL {?x0 dbpprop:出生地 ?birthplace_name3.}\n" \
			u"  OPTIONAL {?x0 dbpprop:birthPlace ?birthplace_name4.}\n" \
			u"  OPTIONAL {?x0 dbpprop:出生日期 ?birthday1.}\n" \
			u"  OPTIONAL {?x0 dbpprop:birthdate ?birthday2.}\n" \
			u"  OPTIONAL {?x0 dbpprop:birthDate ?birthday3.}\n" \
			u"  OPTIONAL {?x0 dbpprop:母校 ?university_link.\n" \
			u"            ?university_link rdfs:label ?university_name}\n" \
			u"  OPTIONAL {?x0 foaf:depiction ?picture.}\n" \
			u"}"

	body_short = u"SELECT DISTINCT ?answer FROM <http://zh.dbpedia.org> WHERE {\n"

	body_short += u"  ?x1 dbpprop:director ?x0.\n" \
			u"  ?x0 rdfs:label ?answer.\n" \
			u"  FILTER (?x1=<http://zh.dbpedia.org/resource/" + name + u">)\n" \
			u"}\n\n"

	return prefix + body_short + "###\n\n" + prefix + body

def generate_query_for_starring(s):
	pattern1 = re.compile(ur"谁主演了?(.+)")
	pattern2 = re.compile(ur"谁是(.+)的主演")
	name = re.findall(pattern1, s)
	if len(name) == 0:
		name = name = re.findall(pattern2, s)
	if len(name) != 0:
		name = name[0]

	prefix = add_prefix()

	body = u"SELECT DISTINCT ?answer ?name ?comment ?birthplace_name1 ?birthplace_name2 ?birthplace_name3 ?birthplace_name4" \
		   u" ?birthday1 ?birthday2 ?birthday3 ?university_name ?picture FROM <http://zh.dbpedia.org> WHERE {\n"

	body += u"  ?x1 dbpprop:starring ?x0.\n" \
			u"  ?x0 rdfs:label ?answer.\n" \
			u"  FILTER (?x1=<http://zh.dbpedia.org/resource/" + name + u">)\n" \
			u"  OPTIONAL {?x0 rdfs:comment ?comment.}\n" \
			u"  ?x0 rdfs:label ?name.\n" \
			u"  OPTIONAL {?x0 dbpprop:出生地點 ?birthplace_name1.}\n" \
			u"  OPTIONAL {?x0 dbpprop:出生地点 ?birthplace_name2.}\n" \
			u"  OPTIONAL {?x0 dbpprop:出生地 ?birthplace_name3.}\n" \
			u"  OPTIONAL {?x0 dbpprop:birthPlace ?birthplace_name4.}\n" \
			u"  OPTIONAL {?x0 dbpprop:出生日期 ?birthday1.}\n" \
			u"  OPTIONAL {?x0 dbpprop:birthdate ?birthday2.}\n" \
			u"  OPTIONAL {?x0 dbpprop:birthDate ?birthday3.}\n" \
			u"  OPTIONAL {?x0 dbpprop:母校 ?university_link.\n" \
			u"            ?university_link rdfs:label ?university_name}\n" \
			u"  OPTIONAL {?x0 foaf:depiction ?picture.}\n" \
			u"}"

	body_short = u"SELECT DISTINCT ?answer  FROM <http://zh.dbpedia.org> WHERE {\n"

	body_short += u"  ?x1 dbpprop:starring ?x0.\n" \
			u"  ?x0 rdfs:label ?answer.\n" \
			u"  FILTER (?x1=<http://zh.dbpedia.org/resource/" + name + u">)\n" \
			u"}\n\n"

	return prefix + body_short + "###\n\n" + prefix + body

def generate_query_for_author(s):
	pattern1 = re.compile(ur"谁写了(.+)")
	pattern2 = re.compile(ur"^谁是(.+)的作者")
	pattern3 = re.compile(ur"(.+)是谁写的")
	name = re.findall(pattern1, s)
	if len(name) == 0:
		name = re.findall(pattern2, s)
	if len(name) == 0:
		name = re.findall(pattern3, s)
	if len(name) != 0:
		name = name[0]

	prefix = add_prefix()

	body = u"SELECT DISTINCT ?answer ?name ?comment ?birthplace_name1 ?birthplace_name2 ?birthplace_name3 ?birthplace_name4" \
		   u" ?birthday1 ?birthday2 ?birthday3 ?university_name ?picture FROM <http://zh.dbpedia.org> WHERE {\n"

	body += u"  ?x1 dbpprop:author ?x0.\n" \
			u"  ?x0 rdfs:label ?answer.\n" \
			u"  FILTER (?x1=<http://zh.dbpedia.org/resource/" + name + u">)\n" \
			u"  OPTIONAL {?x0 rdfs:comment ?comment.}\n" \
			u"  ?x0 rdfs:label ?name.\n" \
			u"  OPTIONAL {?x0 dbpprop:出生地點 ?birthplace_name1.}\n" \
			u"  OPTIONAL {?x0 dbpprop:出生地点 ?birthplace_name2.}\n" \
			u"  OPTIONAL {?x0 dbpprop:出生地 ?birthplace_name3.}\n" \
			u"  OPTIONAL {?x0 dbpprop:birthPlace ?birthplace_name4.}\n" \
			u"  OPTIONAL {?x0 dbpprop:出生日期 ?birthday1.}\n" \
			u"  OPTIONAL {?x0 dbpprop:birthdate ?birthday2.}\n" \
			u"  OPTIONAL {?x0 dbpprop:birthDate ?birthday3.}\n" \
			u"  OPTIONAL {?x0 dbpprop:母校 ?university_link.\n" \
			u"            ?university_link rdfs:label ?university_name}\n" \
			u"  OPTIONAL {?x0 foaf:depiction ?picture.}\n" \
			u"}"

	body_short = u"SELECT DISTINCT ?answer FROM <http://zh.dbpedia.org> WHERE {\n"

	body_short += u"  ?x1 dbpprop:author ?x0.\n" \
			u"  ?x0 rdfs:label ?answer.\n" \
			u"  FILTER (?x1=<http://zh.dbpedia.org/resource/" + name + u">)\n" \
			u"}\n\n"
	return prefix + body_short + "###\n\n" + prefix + body


def generate_query_for_capital(s):
	pattern1 = re.compile(ur"(.+)的首都(在|是)哪里")
	name = re.findall(pattern1, s)[0][0]

	prefix = add_prefix()

	body = u"SELECT DISTINCT ?answer ?name ?comment ?area1 ?area2 ?population1 ?population2" \
		   u"?longitude_num ?longitude_dire ?latitude_num ?latitude_dire ?picture FROM <http://zh.dbpedia.org> WHERE {\n"

	body += u"  ?x1 dbpprop:capital ?x0.\n"\
			u"  FILTER (?x1=<http://zh.dbpedia.org/resource/" + name + u">).\n" \
			u"  ?x0 rdfs:label ?answer.\n" \
			u"  ?x0 rdfs:label ?name.\n" \
			u"  OPTIONAL {?x0 rdfs:comment ?comment.}\n" \
			u"  OPTIONAL {?x0 dbpprop:总面积 ?area1.}\n" \
			u"  OPTIONAL {?x0 dbpprop:areaTotalKm ?area2.}\n" \
			u"  OPTIONAL {?x0 dbpprop:人口 ?population1}\n" \
			u"  OPTIONAL {?x0 dbpprop:populationBlank ?population2}\n" \
			u"  OPTIONAL {?x0 dbpprop:longd ?longitude_num}\n" \
			u"  OPTIONAL {?x0 dbpprop:longew ?longitude_dire}\n" \
			u"  OPTIONAL {?x0 dbpprop:latd ?latitude_num}\n" \
			u"  OPTIONAL {?x0 dbpprop:latns ?latitude_dire}\n" \
			u"  OPTIONAL {?x0 foaf:depiction ?picture}\n" \
			u"}"

	body_short = u"SELECT DISTINCT ?answer FROM <http://zh.dbpedia.org> WHERE {\n"

	body_short += u"  ?x1 dbpprop:capital ?x0.\n" \
			u"  FILTER (?x1=<http://zh.dbpedia.org/resource/" + name + u">).\n" \
			u"  ?x0 rdfs:label ?answer.\n" \
			u"}\n\n"

	return prefix + body_short + "###\n\n" + prefix + body


def generate_query_for_from(s):
	pattern1 = re.compile(ur"(.+)来自哪里")
	name = re.search(pattern1, s).group(1)

	prefix = add_prefix()

	body = u"SELECT DISTINCT ?answer ?name ?comment ?area1 ?area2 ?population1 ?population2" \
		   u"?longitude_num ?longitude_dire ?latitude_num ?latitude_dire ?picture FROM <http://zh.dbpedia.org> WHERE {\n"

	body += u"  ?x1 dbpprop:出生地點 ?answer.\n" \
			u"  FILTER (?x1=<http://zh.dbpedia.org/resource/" + name + u">).\n" \
			u"  ?x1 dbpprop:出生地點 ?x0.\n" \
			u"  OPTIONAL {?x0 rdfs:label ?name.}\n" \
			u"  OPTIONAL {?x0 rdfs:comment ?comment.}\n" \
			u"  OPTIONAL {?x0 dbpprop:总面积 ?area1.}\n" \
			u"  OPTIONAL {?x0 dbpprop:areaTotalKm ?area2.}\n" \
			u"  OPTIONAL {?x0 dbpprop:人口 ?population1}\n" \
			u"  OPTIONAL {?x0 dbpprop:populationBlank ?population2}\n" \
			u"  OPTIONAL {?x0 dbpprop:longd ?longitude_num}\n" \
			u"  OPTIONAL {?x0 dbpprop:longew ?longitude_dire}\n" \
			u"  OPTIONAL {?x0 dbpprop:latd ?latitude_num}\n" \
			u"  OPTIONAL {?x0 dbpprop:latns ?latitude_dire}\n" \
			u"  OPTIONAL {?x0 foaf:depiction ?picture}\n" \
			u"}"

	body_short = u"SELECT DISTINCT ?answer FROM <http://zh.dbpedia.org> WHERE {\n"

	body_short += u"  ?x1 dbpprop:出生地點 ?answer.\n" \
			u"  FILTER (?x1=<http://zh.dbpedia.org/resource/" + name + u">).\n" \
			u"}\n\n"

	return prefix + body_short + "###\n\n" + prefix + body

