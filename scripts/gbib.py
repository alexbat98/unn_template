# coding=utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import sys
import json
import codecs


def extract_main_name(authors):
    authors = item["author"].split(',')
    main_author = authors[0].strip().split(' ')
    return main_author[-1]


def comp(obj1, obj2):
    if obj1["lang"] == "russian" and obj2["lang"] != "russian":
        return -1
    elif obj1["lang"] != "russian" and obj2["lang"] == "russian":
        return 1
    else:
        if "authors" in obj1 and "authors" in obj2:
            name1 = extract_main_name(obj1["authors"])
            name2 = extract_main_name(obj2["authors"])
            if name1 > name2:
                return 1
            elif name1 < name2:
                return -1
            else:
                return 0
        else:
            return 0



def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def print_as_is(item):
    bibitem = "\\bibitem{" + item["id"] + "}\n"
    bibitem += item["asis"]
    bibitem += "\n"
    return bibitem


def print_rus_three_less(item):
    authors = item["author"].split(',')

    main_author = authors[0].strip().split(' ')
    main_author_str = main_author[len(main_author) - 1] + ", "
    for i in main_author[:-1]:
        main_author_str += i[0] + '.'

    all_authors = []
    for author in authors:
        author_parts = author.strip().split(" ")
        auth_str = ""
        for part in author_parts[:-1]:
            auth_str += part[0] + "."
        auth_str += " " + author_parts[len(author_parts) - 1]
        all_authors.append(auth_str)

    bibitem = "\\bibitem{" + item["id"] + "}\n"
    bibitem += main_author_str + " " + item["title"] + " / "

    all_authors_str = ", ".join(all_authors) + "."

    bibitem += all_authors_str + " " + item["city"] + ": "
    bibitem += item["publisher"] + ", " + item["year"] + "."
    bibitem += " - " + item["pages"] + " с. \n"

    return bibitem


def main():
    f = codecs.open(sys.argv[2], 'w', "utf-8")
    f.write("\\clearpage\n")
    f.write("\\begingroup\n")
    f.write("\\phantomsection\n")
    # f.write("\\renewcommand{\section}[2]{\\anonsection{Список литературы}}\n")
    f.write("\\addcontentsline{toc}{section}{Список литературы}\n")
    f.write("\\begin{thebibliography}{00}\n")

    bibf = codecs.open(sys.argv[1], 'r', "utf-8")
    data = json.load(bibf)
    bibf.close()

    data = sorted(data, key=cmp_to_key(comp))

    for item in data:
        if "asis" in item:
            f.write(print_as_is(item))
        elif "lang" not in item or item["lang"] == "russian":
            if "author" in item:
                if len(item["author"].split(',')) <= 3:
                    f.write(print_rus_three_less(item))

    f.write("\\end{thebibliography}\n")
    f.write("\\endgroup\n")
    f.close()

if __name__ == "__main__":
    main()
