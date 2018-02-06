#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Main script for DBpedia quepy.
"""

import sys
import time
import random
import datetime
import re
import nltk

import quepy
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
dbpedia = quepy.install("dbpedia")

# quepy.set_loglevel("DEBUG")


def print_define(results, target, metadata=None):
    for result in results["results"]["bindings"]:
        if result[target]["xml:lang"] == "en":
            print (result[target]["value"])
            print


def print_enum(results, target, metadata=None):
    used_labels = []

    for result in results["results"]["bindings"]:
        if result[target]["type"] == u"literal":
            if result[target]["xml:lang"] == "en":
                label = result[target]["value"]
                if label not in used_labels:
                    used_labels.append(label)
                    print (label)


def print_literal(results, target, metadata=None):
    for result in results["results"]["bindings"]:
        literal = result[target]["value"]
        if metadata:
            print (metadata.format(literal))
        else:
            print (literal)


def print_time(results, target, metadata=None):
    gmt = time.mktime(time.gmtime())
    gmt = datetime.datetime.fromtimestamp(gmt)

    for result in results["results"]["bindings"]:
        offset = result[target]["value"].replace(u"−", u"-")

        if ("to" in offset) or ("and" in offset):
            if "to" in offset:
                connector = "and"
                from_offset, to_offset = offset.split("to")
            else:
                connector = "or"
                from_offset, to_offset = offset.split("and")

            from_offset, to_offset = int(from_offset), int(to_offset)

            if from_offset > to_offset:
                from_offset, to_offset = to_offset, from_offset

            from_delta = datetime.timedelta(hours=from_offset)
            to_delta = datetime.timedelta(hours=to_offset)

            from_time = gmt + from_delta
            to_time = gmt + to_delta

            location_string = random.choice(["where you are",
                                             "your location"])

            print ("Between %s %s %s, depending on %s" % \
                  (from_time.strftime("%H:%M"),
                   connector,
                   to_time.strftime("%H:%M on %A"),
                   location_string))

        else:
            offset = int(offset)

            delta = datetime.timedelta(hours=offset)
            the_time = gmt + delta

            print (the_time.strftime("%H:%M on %A"))


def print_age(results, target, metadata=None):
    assert len(results["results"]["bindings"]) == 1

    birth_date = results["results"]["bindings"][0][target]["value"]
    year, month, days = birth_date.split("-")

    birth_date = datetime.date(int(year), int(month), int(days))

    now = datetime.datetime.utcnow()
    now = now.date()

    age = now - birth_date
    print ("{} years old".format(age.days / 365))


def wikipedia2dbpedia(wikipedia_url):
    """
    Given a wikipedia URL returns the dbpedia resource
    of that page.
    """

    query = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT * WHERE {
        ?url foaf:isPrimaryTopicOf <%s>.
    }
    """ % wikipedia_url

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if not results["results"]["bindings"]:
        print ("Snorql URL not found")
        sys.exit(1)
    else:
        return results["results"]["bindings"][0]["url"]["value"]


def judge_who_verb(question):
    text = nltk.word_tokenize(question)
    res = nltk.pos_tag(text)
    if res[0][0].lower() == "who" and res[1][1] == "VBD":
        return True
    return False


def modify_query_by_who_of(query, target):
    query = query.replace(target, "?answer")
    query = query.replace("DISTINCT ?answer",
                          "DISTINCT ?answer ?name ?comment ?birthplace_name ?birthday ?university_name ?picture")

    target = "?answer"
    entity_pattern = re.compile("\s(.+?)\s[a-z]+\:[a-z]+\s\?answer")
    try:
        target_entity = re.search(entity_pattern, query).group(1).strip()
    except:
        return None
    # print target_entity
    query = query.replace("foaf:name", "rdfs:label")
    pattern_str = "}"
    target_str = "  OPTIONAL {" + target_entity + " rdfs:comment ?comment}.\n\
  OPTIONAL {" + target_entity + " rdfs:label ?name.}\n\
  OPTIONAL {" + target_entity + " dbpprop:birthPlace ?birthplace_name.}\n\
  OPTIONAL {" + target_entity + " dbpprop:birthDate ?birthday.}\n\
  OPTIONAL {" + target_entity + " dbpedia:almaMater ?university_link.\n\
            ?university_link rdfs:label ?university_name}\n\
  OPTIONAL {" + target_entity + " foaf:depiction ?picture.}\n}"
    query = query.replace(pattern_str, target_str)
    return query


def modify_query_by_who(query, target):
    query = query.replace(target, "?answer")
    query = query.replace("foaf:name", "rdfs:label")
    query = query.replace("DISTINCT ?answer", "DISTINCT ?answer ?name ?comment ?birthplace_name ?birthday ?university_name ?picture")

    pattern_str = "}"
    target_str = "  ?x0 rdfs:comment ?comment.\n\
  ?x0 rdfs:label ?name.\n\
  OPTIONAL {?x0 dbpprop:birthPlace ?birthplace_name.}\n\
  OPTIONAL {?x0 dbpprop:birthDate ?birthday.}\n\
  OPTIONAL {?x0 dbpedia:almaMater ?university_link.\n\
            ?university_link rdfs:label ?university_name}\n\
  OPTIONAL {?x0 foaf:depiction ?picture.}\n}"

    query = query.replace(pattern_str, target_str)
    return query


def judge_where_type(question):
    text = nltk.word_tokenize(question)
    res = nltk.pos_tag(text)
    tag_ans = ""
    for pair in res:
        tag_ans += (pair[1] + " ")

    pattern1 = re.compile(r"WRB VBZ (DT |NNP )+IN (\. )?")
    if re.match(pattern1, tag_ans):
        return "where_from"
    pattern2 = re.compile(r"WRB VBZ (DT |NNP )+(\.)?")
    if re.match(pattern2, tag_ans):
        return "where_is"
    return "where"


def modify_query_by_where_from(query, target):
    query = query.replace(target, "?answer")
    query = query.replace("DISTINCT ?answer", "DISTINCT ?answer ?name ?comment ?area1 ?area2 ?population \
?longitude_num ?longitude_dire ?latitude_num ?latitude_dire ?picture")

    pattern_str = "}"
    target_str = "  ?x1 rdfs:label ?name.\n\
  OPTIONAL {?x1 rdfs:comment ?comment.}\n\
  OPTIONAL {?x1 dbpprop:areaKM ?area1.}\n\
  OPTIONAL {?x1 dbpprop:areaTotalKm ?area2.}\n\
  OPTIONAL {?x1 dbpprop:populationTotal ?population}\n\
  OPTIONAL {?x1 dbpprop:longd ?longitude_num}\n\
  OPTIONAL {?x1 dbpprop:longew ?longitude_dire}\n\
  OPTIONAL {?x1 dbpprop:latd ?latitude_num}\n\
  OPTIONAL {?x1 dbpprop:latns ?latitude_dire}\n\
  OPTIONAL {?x1 foaf:depiction ?picture}\n}"
    query = query.replace(pattern_str, target_str)
    return query


def modify_query_by_where_is(query, target):
    query = query.replace(target, "?answer")
    query = query.replace("DISTINCT ?answer", "DISTINCT ?answer ?name ?comment ?area1 ?area2 ?population \
?longitude_num ?longitude_dire ?latitude_num ?latitude_dire ?picture")
    query = query.replace("quepy:Keyword", "rdfs:label")
    pattern_str = re.compile(r"\?x0\sdbpedia\-owl\:location.+\}", re.S)
    target_str = "?x0 rdf:type dbpedia:Place .\n\
  ?x0 rdfs:comment ?answer.\n\
  ?x0 rdfs:label ?name.\n\
  OPTIONAL {?x0 rdfs:comment ?comment.}\n\
  OPTIONAL {?x0 dbpprop:areaKM ?area1.}\n\
  OPTIONAL {?x0 dbpprop:areaTotalKm ?area2.}\n\
  OPTIONAL {?x0 dbpprop:populationTotal ?population}\n\
  OPTIONAL {?x0 dbpprop:longd ?longitude_num}\n\
  OPTIONAL {?x0 dbpprop:longew ?longitude_dire}\n\
  OPTIONAL {?x0 dbpprop:latd ?latitude_num}\n\
  OPTIONAL {?x0 dbpprop:latns ?latitude_dire}\n\
  OPTIONAL {?x0 foaf:depiction ?picture}\n}"
    query = re.sub(pattern_str, target_str, query)
    #print query
    return query


def judge_what_type(question, query):
    question_pattern = re.compile(r"what (is|are) the .+ of .+")
    if re.match(question_pattern, question):
        query_pattern = re.compile(r"(\?x[0-9]) rdf:type dbpedia-owl:([a-zA-Z]+).")
        question_type = re.search(query_pattern, query).group(2)
        target_var = re.search(query_pattern, query).group(1)
        print target_var, question_type
        return target_var, "what_" + question_type
    else:
        return None, "what"


def modify_query_by_what_of_tvshow(query, target_entity, target):
    query = query.replace(target, "?answer")
    query = query.replace("DISTINCT ?answer", "DISTINCT ?answer ?name ?comment ?runtime "
                                              "?country ?language ?releaseDate ?producer ?director ?picture")

    pattern_str = "}"
    target_str = "  OPTIONAL {" + target_entity + " rdfs:comment ?comment}.\n\
  OPTIONAL {" + target_entity + " rdfs:label ?name.}\n\
  OPTIONAL {" + target_entity + " dbpprop:runtime ?runtime.}\n\
  OPTIONAL {" + target_entity + " dbpprop:language ?language.}\n\
  OPTIONAL {" + target_entity + " dbpprop:country ?country.}\n\
  OPTIONAL {" + target_entity + " dbpedia:releaseDate ?releaseDate.}\n\
  OPTIONAL {" + target_entity + " dbpprop:producer ?producer.}\n\
  OPTIONAL {" + target_entity + " dbpprop:director ?director.}\n\
  OPTIONAL {" + target_entity + " foaf:depiction ?picture.}\n}"
    query = query.replace(pattern_str, target_str)
    return query


def modify_query_by_what_of_place(query, target_entity, target):
    query = query.replace(target, "?answer")
    query = query.replace("DISTINCT ?answer", "DISTINCT ?answer ?name ?comment ?area1 ?area2 ?population \
  ?longitude_num ?longitude_dire ?latitude_num ?latitude_dire ?picture")
    pattern_str = "}"
    target_str = "  ?x0 rdfs:label ?name.\n\
  OPTIONAL {" + target_entity + " rdfs:comment ?comment.}\n\
  OPTIONAL {" + target_entity + " dbpprop:areaKm ?area1.}\n\
  OPTIONAL {" + target_entity + " dbpedia:areaTotal ?area2.}\n\
  OPTIONAL {" + target_entity + " dbpedia:populationTotal ?population}\n\
  OPTIONAL {" + target_entity + " dbpprop:longd ?longitude_num}\n\
  OPTIONAL {" + target_entity + " dbpprop:longew ?longitude_dire}\n\
  OPTIONAL {" + target_entity + " dbpprop:latd ?latitude_num}\n\
  OPTIONAL {" + target_entity + " dbpprop:latns ?latitude_dire}\n\
  OPTIONAL {" + target_entity + " foaf:depiction ?picture}\n}"

    query = query.replace(pattern_str, target_str)
    return query


def modify_query_by_what_of_band(query, target_entity, target):
    query = query.replace(target, "?answer")
    query = query.replace("DISTINCT ?answer", "DISTINCT ?answer ?name ?comment ?band_type ?currentMembers "
                                              "?style_description ?origin ?picture")
    pattern_str = "}"
    target_str = "  ?x0 rdfs:label ?name.\n\
  OPTIONAL {" + target_entity + " rdfs:comment ?comment.}\n\
  OPTIONAL {" + target_entity + " dbpedia:background ?band_type.}\n\
  OPTIONAL {" + target_entity + " dbpedia:populationTotal ?population}\n\
  OPTIONAL {" + target_entity + " dbpprop:currentMembers ?currentMembers}\n\
  OPTIONAL {" + target_entity + " dbpprop:description ?style_description}\n\
  OPTIONAL {" + target_entity + " dbpprop:origin ?origin}\n\
  OPTIONAL {" + target_entity + " foaf:depiction ?picture}\n}"
    query = query.replace(pattern_str, target_str)
    return query


def generate_query(question=None):

    print_handlers = {
        "define": print_define,
        "enum": print_enum,
        "time": print_time,
        "literal": print_literal,
        "age": print_age,
    }

    queries = []

    #for question in questions:
    print (question)
    print ("-" * len(question))

    target, query, metadata = dbpedia.get_query(question)
    old_query = query
    # print "query: ", query
    if not query:
        print "Query not generated for that question, try again with another question please."
        return "Query not generated for that question, try again with another question please."
    query = query.replace("WHERE", "FROM <http://dbpedia.org> WHERE")
    query = query.replace("dbpprop:populationCensus", "dbpedia:populationTotal")


    if "who " in question.lower():
        pattern1 = re.compile(r"who (is|are) .+ of")
        if re.match(pattern1, question.lower()):
            new_query = modify_query_by_who_of(query, target.strip())
        elif judge_who_verb(question):
            new_query = modify_query_by_who_of(query, target.strip())
        else:
            new_query = modify_query_by_who(query, target.strip())
    elif "where " in question.lower():
        where_type = judge_where_type(question)
        if where_type == "where_from":
            new_query = modify_query_by_where_from(query, target.strip())
        elif where_type == "where_is":
            new_query = modify_query_by_where_is(query, target.strip())
        else:
            new_query = query.replace(target.strip(), "?answer")
    elif "what" in question.lower():
        # print "What type question"
        target_var, what_type = judge_what_type(question.lower(), query)
        if what_type == "what_TelevisionShow" or what_type == "what_Film":
            print "what_type:", what_type
            new_query = modify_query_by_what_of_tvshow(query, target_var, target.strip())
        elif what_type == "what_Country" or what_type == "what_PopulatedPlace":
            print "what_type:", what_type
            new_query = modify_query_by_what_of_place(query, target_var, target.strip())
        elif what_type == "what_Band":
            print "what_type:", what_type
            new_query = modify_query_by_what_of_band(query, target_var, target.strip())
        else:
            new_query = query.replace(target.strip(), "?answer")
    else:
        new_query = query.replace(target.strip(), "?answer")
    print new_query

    print old_query + "###" + new_query
    return old_query + "###" + new_query


if __name__ == "__main__":
    generate_query("Where is Beijing")
