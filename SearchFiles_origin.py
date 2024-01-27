#!/usr/bin/env python



INDEX_DIR = "IndexFiles.index"

import sys, os, lucene,math
from org.apache.lucene.analysis.cjk import CJKAnalyzer
from java.io import File
from java.nio.file import Path
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.search.highlight import Highlighter,QueryScorer,SimpleFragmenter,SimpleHTMLFormatter
"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def init():
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

def parseCommand(command):
    '''
    input: C title:T author:A language:L
    output: {'contents':C, 'title':T, 'author':A, 'language':L}

    Sample:
    input:'contenance title:henri language:french author:william shakespeare'
    output:{'author': ' william shakespeare',
                   'language': ' french',
                   'contents': ' contenance',
                   'title': ' henri'}
    '''
    allowed_opt = ['url','platform','sort','price_range']
    command_dict = {}
    opt = 'name'
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            command_dict[opt] = command_dict.get(opt, '') + ' ' + i
    return command_dict

def run(searcher, analyzer, keyword, page):
    # while True:
    #     print()
        # print ("Hit enter with no input to quit.")
        # command = input("Query:")
    command = keyword
        # command = unicode(command, 'GBK')
        # if command == '':
        #     return

        # print()
        # print ("Searching for:", command)
        
    command_dict = parseCommand(command)
    querys = BooleanQuery.Builder()
    for k,v in command_dict.items():
        if(k!='sort' and k!='price_range'):
            query = QueryParser(k, analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)
        #elif k=='price_range':
            #query= 
    scoreDocs1 = searcher.search(querys.build(),500).scoreDocs
    scoreDocs = [i for i in scoreDocs1]
    if(command_dict.get('price_range', '')!=''):
        l,h=command_dict.get('price_range', '').split(',')[:2]
        h=float(h)
        l=float(l)
        i=0
        while(i<len(scoreDocs)):
            price=float(searcher.doc(scoreDocs[i].doc).get("price"))
            if price>h or price<l:
                scoreDocs.pop(i)
            else:
                i+=1

    avg = 1
    for x in scoreDocs:
        avg += float(searcher.doc(x.doc).get("price"))
    try:
        avg /= len(scoreDocs)
    except:
        avg=1
    if('comprehensive' in command_dict.get('sort', '')):
        _, n = command_dict.get('sort', '').split(',')[:2]
        n = float(n)
        scoreDocs = sorted(scoreDocs, key=lambda x: x.score +
                               (0.5-n)*math.log(float(searcher.doc(x.doc).get("price"))/avg+1, 5)+n * float(
                                   searcher.doc(x.doc).get("score")), reverse=True)
    if('score' in command_dict.get('sort','')):
        scoreDocs = sorted(scoreDocs, key=lambda x: float(
            searcher.doc(x.doc).get("score")), reverse=True)
    if('price_d' in command_dict.get('sort', '')):
        scoreDocs=sorted(scoreDocs,key=lambda x:float(searcher.doc(x.doc).get("price")),reverse=True)
    if('price_i' in command_dict.get('sort', '')):
        scoreDocs=sorted(scoreDocs,key=lambda x:float(searcher.doc(x.doc).get("price")))
    print("%s total matching documents." % len(scoreDocs))
    #formatter = SimpleHTMLFormatter("<font color='red'>", "</font>")
    #highlighter = Highlighter(formatter, QueryScorer(query))
    #highlighter.setTextFragmenter(SimpleFragmenter(10))

    results = []
    for scoreDoc in scoreDocs[50*page:50*(page+1)]:
        result = {}
        doc = searcher.doc(scoreDoc.doc)
        explanation = searcher.explain(query, scoreDoc.doc)
        # print("------------------------")
        #print('path:', doc.get("path"))
        #print('name:', doc.get("name"))
        # print('name:', doc.get('name'))
        # print('img:', doc.get('img'))
        # print('price:', doc.get('price'))
        # print('shop:', doc.get('shop'))
        # print('url:', doc.get('url'))
        # print('relscore:', scoreDoc.score)
        # print('score:',doc.get('score'))
        # print('shopurl:',doc.get('shopurl'))
        result['name'] = doc.get('name')
        result['img'] = doc.get('img')
        result['price'] = doc.get('price')
        result['shop'] = doc.get('shop')
        result['url'] = doc.get('url')
        if doc.get('platform') == 'jd':
            result['platform'] = '京东'
        elif doc.get('platform') == 'tm':
            result['platform'] = '天猫'
        elif doc.get('platform') == 'sn':
            result['platform'] = '苏宁'
        result['score'] = doc.get('score')

        results.append(result)
        
        #print (explanation)
    # print("%s total matching documents." % len(scoreDocs))
    return len(scoreDocs), results
    
def search(keyword,l,h,sort, page):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_all"
    # print('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = CJKAnalyzer()
    search_key=keyword+" price_range:{},{} sort:{}".format(l,h,sort)
    return run(searcher, analyzer, search_key, page)

if __name__ == '__main__':
    init()
    STORE_DIR = "index_all"
    print('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = CJKAnalyzer()
    keyword = "手机 platform:sn"
    page = 0
    run(searcher, analyzer, keyword, page)
