#!/usr/bin/env python3

import os
import sys
import argparse
import textwrap
from pathlib import Path

BIBLIB_DIR = os.path.join(os.path.dirname(Path(__file__).resolve()), 'biblib')
sys.path.append(BIBLIB_DIR)

try:
    import biblib.bib
    import biblib.algo
except ModuleNotFoundError as ex:
    print(ex, file=sys.stderr)
    print(textwrap.dedent(f"""
    Error: could not load the 'biblib' library.
    To fix this do *one* of the following:

    First Option: install clone 'biblib' locally by running:

        git clone https://github.com/aclements/biblib {BIBLIB_DIR.rstrip('/')}/

    Second Option: install 'publistgen' by running: python setup.py install

    """), file=sys.stderr)
    sys.exit(1)

def load_bib(bibtex_filehandle):
    try:
        # Load databases
        parser = biblib.bib.Parser()
        db = parser.parse(bibtex_filehandle,
                          log_fp=sys.stderr)
        db = db.get_entries()
        db = biblib.bib.resolve_crossrefs(db)
        return db
    except biblib.messages.InputError:
        print("InputError")
        sys.exit(1)

author_homepages = {
'Sergey Goncharov': "http://www8.informatik.uni-erlangen.de/~sergey/",
'Lutz Schröder': "http://www8.informatik.uni-erlangen.de/schroeder/",
'Stefan Milius': "https://www8.cs.fau.de/milius",
'Tadeusz Litak': "http://www8.informatik.uni-erlangen.de/~litak/",
'Daniel Gorín': "http://www8.informatik.uni-erlangen.de/~gorin/",
'Thorsten Wißmann': "http://www8.informatik.uni-erlangen.de/thorsten",
'Dirk Pattinson': "http://users.cecs.anu.edu.au/~dpattinson/",
'Ulrich Dorsch': "https://www8.cs.fau.de/ulrich",
'Dexter Kozen': "http://www.cs.cornell.edu/~kozen/",
'Harsh Beohar': "http://www.ti.inf.uni-due.de/people/beohar/",
'Barbara König': "http://www.ti.inf.uni-due.de/people/koenig/",
'Sebastian Küpper': "http://www.fernuni-hagen.de/mi/lehrende/kuepper/index.shtml",
'Alexandra Silva': "http://www.alexandrasilva.org/#/main.html",
'Hans-Peter Deifel': "https://www8.cs.fau.de/deifel",
'Jérémy Dubut': "http://group-mmm.org/~dubut/",
'Shin-ya Katsumata': "http://group-mmm.org/~s-katsumata/index-e.html",
'Lurdes Sousa': "http://www.estgv.ipv.pt/paginaspessoais/sousa/",
'Ichiro Hasuo': "https://group-mmm.org/~ichiro/",
#'Jiří Adámek': "https://www.tu-braunschweig.de/iti/mitarbeiter/adamek/",
'Jiří Adámek': "https://dblp.uni-trier.de/pers/hd/a/Ad=aacute=mek:Jir=iacute=",
}

def bibentry2html(ent):
    global auth_urls
    authors = [
        biblib.algo.tex_to_unicode(author.pretty(),
                                   pos=ent.field_pos['author'])
        for author in ent.authors()]
    auth_urls = []
    for a in authors:
        if a in author_homepages:
            hp = author_homepages[a]
            auth_urls.append('<a target="_blank" href="{}">{}</a>'.format(hp, a))
        else:
            auth_urls.append(a)
    pubplace = "???"
    for pp in ['journal', 'booktitle']:
        if pp in ent:
            pubplace = '<i>' + ent[pp] + '</i>'
            break
    if 'volume' in ent:
        pubplace += ", " + ent['volume']
    if 'issue' in ent:
        pubplace += ", " + ent['issue']
    if 'pages' in ent:
        pubplace += ", pp. " + ent['pages']
    if 'note' in ent:
        pubplace += " ({})".format(ent['note'])
    extraurls = ""
    if 'url' in ent:
        extraurls += ' [<a href="{}">PDF</a>]'.format(ent['url'])
    if 'preprinturl' in ent:
        extraurls += ' [<a href="{}">Preprint PDF</a>]'.format(ent['preprinturl'])
    if 'doi' in ent:
        doi = ent['doi']
        extraurls += ' [<a href="https://dx.doi.org/{}">DOI: {}</a>]'.format(doi, doi)
    formatvars = {
        'mainurl': ent.get('url', ent.get('preprinturl')),
        'title': biblib.algo.tex_to_unicode(ent['title']),
        'bibsource': html_encode(ent.to_bib(month_to_macro=False,wrap_width=None)),
        'authors': ', '.join(auth_urls),
        'extraurls': extraurls,
        'pubplace': biblib.algo.tex_to_unicode(pubplace.replace('\\ ', ' ')),
    }
    s = """\
     <span class="title"><a href="{mainurl}">{title}</a></span>
     (<span class="authors">{authors}</span>)
     <span class="venueline">In: <span class="journal">{pubplace}</span>
     [<a style="cursor: pointer;" onClick="showBibHere(this);">bibtex</a>]
     {extraurls}
     <pre class="bibhidden">
{bibsource}</pre>
    """.format(**formatvars)
    return s


def bibentry2markdown(ent):
    global auth_urls
    authors = [
        biblib.algo.tex_to_unicode(author.pretty(),
                                   pos=ent.field_pos['author'])
        for author in ent.authors()]
    auth_urls = []
    for a in authors:
        if a in author_homepages:
            hp = author_homepages[a]
            auth_urls.append('[{title}]({href})'.format(href=hp, title=a))
        else:
            auth_urls.append(a)
    pubplace = "???"
    for pp in ['journal', 'booktitle']:
        if pp in ent:
            pubplace = '*' + ent[pp] + '*'
            break
    if 'volume' in ent:
        pubplace += ", " + ent['volume']
    if 'issue' in ent:
        pubplace += ", " + ent['issue']
    if 'pages' in ent:
        pubplace += ", pp. " + ent['pages']
    extraurls = ""
    if 'url' in ent:
        extraurls += ' \[[PDF]({})\]'.format(ent['url'])
    if 'preprinturl' in ent:
        extraurls += ' \[[Preprint PDF]({})\]'.format(ent['preprinturl'])
    if 'doi' in ent:
        doi = ent['doi']
        extraurls += ' \[[DOI: {}](https://dx.doi.org/{})\]'.format(doi, doi)
    formatvars = {
        'mainurl': ent.get('url', ent.get('preprinturl')),
        'title': biblib.algo.tex_to_unicode(ent['title']),
        'bibsource': html_encode(ent.to_bib(month_to_macro=False,wrap_width=None)),
        'authors': ', '.join(auth_urls),
        'extraurls': extraurls,
        'pubplace': biblib.algo.tex_to_unicode(pubplace.replace('\\ ', ' ')),
    }
    s = """[{title}]({mainurl}) ({authors}) In: {pubplace} {extraurls}""".format(**formatvars)
    # <pre class="bibhidden"> {bibsource}</pre>
    return s


def html_encode(source):
    return source.replace('<', '&lt;').replace('>', '&gt;')

def month2int(texmonth):
    month_names = 'jan feb mar apr may jun jul aug sep oct nov dec'.split(' ')
    try:
        return 1 + month_names.index(str(texmonth)[0:3].lower())
    except ValueError:
        return int(texmonth)

css_code = """
pre {
    white-space: pre-wrap;       /* Since CSS 2.1 */
    white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
    white-space: -pre-wrap;      /* Opera 4-6 */
    white-space: -o-pre-wrap;    /* Opera 7 */
    word-wrap: break-word;       /* Internet Explorer 5.5+ */
}

.biblist {
    margin: 0px;
}
.biblist tr {
    margin-top: 0.5em;
    margin-bottom: 1em;
}
.biblist .title {
    /* font-variant: small-caps; */
    font-size: 1.0em;
}

.biblist .bibhidden {
    display: none;
    /*
    transform: scaleY(0);
    transition: all 0.25s ease-in;
    overflow: hidden;
    */
}

.biblist .bibvisible {
    display: block;
    /*
    transform: scaleY(1);
    transition: all 0.25s ease-in;
    */
}

.biblist .title a {
    /* font-weight: bold; */
}

.biblist tr {
    background-color: transparent;
    -webkit-transition: all 1s linear;
}

.biblist tr:target {
    background-color: #ffa;
    -webkit-transition: all 1s linear;
}

"""

js_code = """
function showBibHere(biblink) {
    var element = biblink;
    while (element.nodeName.toUpperCase() != 'TR') {
        element = element.parentNode;
    }
    var bibsources = element.getElementsByTagName('pre');
    for (var i = 0; i < bibsources.length; i++) {
        var pre = bibsources[i];
        if (pre.classList.contains("bibhidden")) {
            pre.classList.remove("bibhidden")
            pre.classList.add("bibvisible")
        } else {
            pre.classList.add("bibhidden")
            pre.classList.remove("bibvisible")
        }
    }
}
"""

def bibliography2html(db, year2bibs):
    print("<style>{}</style>".format(css_code))
    print("<script>{}</script>".format(js_code))
    entrynumber = len(db.values())
    for y in sorted(list(year2bibs.keys()), reverse=True):
        entries = year2bibs[y]
        entries = sorted(entries, reverse=True, key=lambda e: month2int(e.get('month', 0)))
        print("<h3>{}</h3>".format(y))
        print('<table cellspacing="0" class="biblist">')

        for e in entries:
            print("""
            <tr id="{}">
             <td class="bibitemanchor" style="min-width: 2em;" align="right" valign="top">
               [<a href="#{}">{}</a>]
             </td>
             <td class="bibitemtext" valign="top">{}</td>
            </tr>
            """.format(e.key,e.key,entrynumber,bibentry2html(e)))
            entrynumber -= 1
        print("</table>")


def bibliography2gitlabmarkdown(db, year2bibs):
    entrynumber = len(db.values())
    for y in sorted(list(year2bibs.keys()), reverse=True):
        entries = year2bibs[y]
        entries = sorted(entries, reverse=True, key=lambda e: month2int(e.get('month', 0)))
        for e in entries:
            print('  - ' + bibentry2markdown(e))


def main():
    with open(sys.argv[1]) as fh:
        db = load_bib(fh)
        #print(db)
        year2bibs = { }
        for ent in db.values():
            year = ent['year']
            if year in year2bibs:
                year2bibs[year].append(ent)
            else:
                year2bibs[year] = [ent]
        bibliography2html(db, year2bibs)
        #bibliography2gitlabmarkdown(db, year2bibs)

main()
