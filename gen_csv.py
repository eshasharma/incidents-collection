import csv,json,sys,os
def gen_csv(neg,pos):
    """
    Generate CSV according to the json stored.
    neg: path to negative directory
    pos: path to postive directory
    
    """
    fout = open('data.csv','w')
    out = csv.writer(fout)
    src = [neg,pos]
    dic = ['no.','type_of_material','news_desk','word_count','document_type','pub_date','byline','isPrivacy'];
    length = len(dic)
    keywords = []
    
    for s in src:
        for filename in os.listdir(s):
            fin = open(s+'/'+filename)
            dat = json.load(fin)
            if dat.has_key('keywords'):
                for st in dat['keywords']:
                    keywords.append(st['value'])
    rank = [0]*(len(keywords))
    dic.extend(sorted(keywords))
    out.writerow(dic)
    cnt = 1
    for s in src:
        ###pos and neg src
        for filename in os.listdir(s):
            ###filename => every file in the directory
            fin = open(s+'/'+filename)
            dat = json.load(fin)
            for i in range(1,length-1):
                
                try:
                    #valid json, key
                    dat[dic[i]]
                except Exception,e:
                    print e
                    ##inject none if key doesn't exists
                    dat[dic[i]]='none'
                finally:
                    ###list item
                    if dic[i] == 'byline':
                        string = ''
                        people =  dat['byline']['person']
                        for person in people:
                            try:
                                lastname = person['lastname']
                                firstname = person['firstname']
                                lastname.encode('ascii')
                                firstname.encode('ascii')
                                name = firstname.title() + ' ' + lastname.title()
                            except Exception,e:
                                try:
                                    name = person['original']
                                except Exception,e:
                                    # print person
                                    name = 'none'
                            string = string + name + ','
                        #to ascii since there are some Spanish name
                        string.encode('ascii')
                        dat['byline'] = string[0:len(string)-1]
                    #modify keywords
                    if dat.has_key('keywords'):
                        for st in dat['keywords']:
                            if 'rank' in st:
                                rank[keywords.index(st['value'])] = st['rank']
                            else:
                                rank[keywords.index(st['value'])] = 1
                    try:
                        dat[dic[i]] = str(dat[dic[i]])
                    except Exception, e:
                        print dat[dic[i]] 
            flag = False
            if s == pos:
                flag = True
            result = [cnt,dat['type_of_material'].lower(),dat['news_desk'].lower(),dat['word_count'].lower(),dat['document_type'].lower(),dat['pub_date'].lower(),dat['byline'],flag]
            result.extend(rank)
            out.writerow(result)
            rank =  [0]*(len(keywords))
            cnt+=1
            fin.close()
gen_csv('dat/NYnegative/json','dat/NYpositive/json')
    
