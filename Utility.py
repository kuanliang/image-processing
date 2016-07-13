import os

def xlsToCsv(path):
    '''transform xls format file to csv format file
    
    Notes: the path should include the last back slash mark
    
    Argvs: path
    
    Return: None
    
    '''
    
    for item in os.listdir(path):
        #print item
        pre, ext = os.path.splitext(item)
        if ext == '.xls':
            print 'processing {}.xls'.format(pre)
            item = path + item
            # print item
            # print pre + '.csv'
            os.rename(item, path + pre + '.csv')
            #print item
    
    
