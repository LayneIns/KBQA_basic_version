# -*- coding: utf-8 -*-
import jieba.posseg as pseg

from people import people_match
from place import place_match


def parsing(s):
    words = pseg.cut(s)
    cut_res = []
    for word, tag in words:
        cut_res.append((word, tag))

    return cut_res


def regex_match(cut_res, s):
    if u"谁" in s:
        return people_match(cut_res, s)
    elif u"哪" in s:
        return place_match(cut_res, s)
    else:
        return "Query not generated for this question"


def generate_query(s):
    s = s.strip(u"？")
    cut_res = parsing(s)
    # for item in cut_res:
    #     print item[0],
    # print "\n"
    return regex_match(cut_res, s)


if __name__ == "__main__":
    print(generate_query(u"英国的首都是哪里"))