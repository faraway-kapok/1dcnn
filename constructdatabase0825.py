import os
import pandas as pd
import numpy as np
import re
import sys
import logging

def list_all_files(rootdir):

    _files = []
    _dir = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
              _dir.append(path)
           if os.path.isfile(path):
                if path.split('/')[-1].startswith('.'):
                    continue
                else:
                    _files.append(path)
    return _files

def list_all_dirs(rootdir):

    _files = []
    _dir = []
    _svg = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
              _dir.append(path)
           if os.path.isfile(path):
                if path.split('/')[-1].startswith('.'):
                    continue
                else:
                    _files.append(path)
    return _dir

def numandlabel(figurename):
    num = list(map(int,re.findall(r"\d+", figurename)))
    label = re.findall(r"[a-z]+", figurename)
    return num, label

def figureclassify(figuredirname):
    nfdic = []
 
    figurelist = list_all_files(figuredirname + '/')
    for figureindex in range(len(figurelist)):
        figureid = figurelist[figureindex].split('/')[-1][:-4]
        num, label = numandlabel(figureid)
        # print(num[0])
        # print(label[0])
        nfdic.append((num, label))
        
    nfdic = sorted(nfdic, key=lambda x:x[0])
    # print(nfdic[0])
    return nfdic

def constructtestdata(testdatabasename, csvdir, figuredirname, userdocid):
    databasename = testdatabasename
    file1 = logging.FileHandler(filename='NaN0808.log', mode='a', encoding='utf-8')
    fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    file1.setFormatter(fmt)

    # 定义日志
    logger1 = logging.Logger(name='nan', level=logging.ERROR)
    logger1.addHandler(file1)
    try:
        
        """获取figure列表，
        fulldataoffigure类型为
                                {
                                    'userid1':[(1,'e'), (2,'ge')]
                                ,
                                
                                    'userid2':[(1,'g'), (2,'b')]
                                }
                            
        """
        # fulldataoffigure = []
        nflist = {}
        nflist[userdocid] = figureclassify(figuredirname)
        # print(nflist)
        # fulldataoffigure.append(nflist)
        # print(list(fulldataoffigure[0])[0]) #userid
        # print(list(fulldataoffigure[0].values())[0]) 
        # print(list(fulldataoffigure[0].values())[0][0][0]) #1,figurenum

        """获取csv文件列表,csvname = userid"""
        # csvnamelist = []
            # print(type(csvname))
        database = pd.read_csv(csvdir) 
        nf = nflist[userdocid]
        for j in range(len(nf)):
            rownum = nf[j][0][0] - 1
            # print(rownum)
            dataid = []
            timestamp = []
            xaxis = []
            quality = []
            datamodel = []
            for k in range(1,len(database.iloc[rownum][1:])+1):
                dataid.append(userdocid)
                timestart = rownum * len(database.iloc[0][1:])
                timeend = (rownum+1) * len(database.iloc[0][1:])
                xaxis.append(database.iloc[rownum][k])
                for k in range(timestart,timeend):
                    # timestamp.append((k+1)/100)
                    timestamp.append(k/100)
                if nf[j][1][0] == "e":
                    quality.append('excellent')
                elif nf[j][1][0] == "g":
                    quality.append('good')
                elif nf[j][1][0] == "ge":
                    quality.append('general')
                elif nf[j][1][0] == 'b':
                    quality.append('bad')
                elif nf[j][1][0] == 's':
                    quality.append('sobad')
                elif nf[j][1][0] == 'n':
                    quality.append('nosignal')
            datamodel.append([dataid, quality, timestamp, xaxis])
            # print(len(datamodel))
            # sys.exit()                    
            # print(datamodel[0][1])
            # print(len(datamodel[0][1]))
            with open(databasename, mode='a') as f:
                for k in range(len(datamodel[0][1])):
                    f.write(str(datamodel[0][0][k]))
                    f.write(',')
                    f.write(str(datamodel[0][1][k]))
                    f.write(',')
                    f.write(str(datamodel[0][2][k]))
                    f.write(',')
                    f.write(str(datamodel[0][3][k]))
                    f.write(';')
                    f.write('\n')
            
    except Exception as e:
            print("the file {0} has {1}".format(userdocid, e))    


def constructfulldata():
    databasename = 'database10252056.txt'

    file1 = logging.FileHandler(filename='NaN0808.log', mode='a', encoding='utf-8')
    fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    file1.setFormatter(fmt)

    # 定义日志
    logger1 = logging.Logger(name='nan', level=logging.ERROR)
    logger1.addHandler(file1)

    # filename = '19826_161010104449'
    # filespath = ("E:/LU/fhr_analyse/completedoc/{0}/{1}.adpcm").format(filename,filename)
    csvrootdir = 'E:/LU/fhr_analyse/test0829csv100hz/egge/'
    csvdirlist = list_all_files(csvrootdir)
    # print(len(csvdirlist))
    figurerootdir = 'E:/LU/fhr_analyse/test0829figure100hz/egge/new/'
    # figurerootdir = 'E:/LU/fhr_analyse/test0829figure100hz/egge/nosignal/'
    try:
        figuredirlist = list_all_dirs(figurerootdir)
        print(len(figuredirlist))
       
        """获取figure列表，
        fulldataoffigure类型为
                                {
                                    'userid1':[(1,'e'), (2,'ge')]
                                ,
                                
                                    'userid2':[(1,'g'), (2,'b')]
                                }
                            
        """
        fulldataoffigure = {}
        for figuredirindex in range(len(figuredirlist)):
            
            figuredirname = figuredirlist[figuredirindex]
            figuredir = figuredirname.split('/')[-1]

            figuredirid = figuredir[:-6]
            # print(figuredirid)
            # print(figuredirname)
            fulldataoffigure[figuredirid] = figureclassify(figuredirname)
        
        print(len(fulldataoffigure))
            
        # print(list(fulldataoffigure[0])[0]) #userid
        # print(list(fulldataoffigure[0].values())[0]) 
        # print(list(fulldataoffigure[0].values())[0][0][0]) #1,figurenum

        """获取csv文件列表,csvname = userid"""
        # csvnamelist = []
        for csvdirindex in range(len(csvdirlist)):
            csvdir = csvdirlist[csvdirindex]
            csvname = csvdir.split('/')[-1][:-4]

            database = pd.read_csv(csvdir)

            nf = fulldataoffigure[csvname]
            if nf != None:
                print(csvname)
                # print(type(nf))
                for j in range(len(nf)):
                    # print(type(nf[j][0][0]))
                    rownum = nf[j][0][0] - 1
                    # print(nf[j][1][0])
                    dataid = []
                    timestamp = []
                    xaxis = []
                    quality = []
                    datamodel = []
                    for k in range(2,len(database.iloc[rownum][1:])+1):
                        dataid.append(csvname)
                        timestart = rownum * len(database.iloc[0][1:])                         
                        timeend = (rownum+1) * len(database.iloc[0][1:])
                        xaxis.append(database.iloc[rownum][k])
                        for k in range(timestart,timeend):
                            timestamp.append((k+1)/100)
                        if nf[j][1][0] == "e":
                            quality.append('excellent')
                        elif nf[j][1][0] == "g":
                            quality.append('good')
                        elif nf[j][1][0] == "ge":
                            quality.append('general')
                        elif nf[j][1][0] == 'b':
                            quality.append('bad')
                        elif nf[j][1][0] == 's':
                            quality.append('sobad')
                        elif nf[j][1][0] == 'n':
                            quality.append('nosignal')
                    datamodel.append([dataid, quality, timestamp, xaxis])
                    # print(len(datamodel))
                    # sys.exit()                    
                    # print(datamodel[0][1])
                    # print(len(datamodel[0][1]))
                    with open(databasename, mode='a') as f:
                        for k in range(len(datamodel[0][1])):
                            f.write(str(datamodel[0][0][k]))
                            f.write(',')
                            f.write(str(datamodel[0][1][k]))
                            f.write(',')
                            f.write(str(datamodel[0][2][k]))
                            f.write(',')
                            f.write(str(datamodel[0][3][k]))
                            f.write(';')
                            f.write('\n')
    
    except Exception as e:
            # print("the file {0} has {1}".format(figuredirid, e))    
            print("the file do not has {0}".format(e))    


if __name__ == "__main__":
    import GlobalVars
    # constructfulldata()
    userdocid = '13068_160826083148'
    testdatabasename = GlobalVars.databasedir + 'database0905.txt'
    figuredirname = GlobalVars.figurepath + userdocid + 'figure/'
    csvdir = GlobalVars.csvpath + userdocid + '.csv'
    constructtestdata(testdatabasename, csvdir, figuredirname, userdocid)
   
    