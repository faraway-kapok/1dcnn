import numpy
import pickle
# import Infiledata
import matplotlib.pyplot as plt
import pandas as pd
import os
import math
import logging

SAMPLE_RATE = 100
CORR_LEN = int(2 * SAMPLE_RATE)
CORR_STEP  = int(0.8 * SAMPLE_RATE)
pointcount = 0


def get_data(data):
    if data > 128:
        data1 = data - 128
    else:
        data1 = 128 - data
    return data1

def get_avg(data):

    sum1=0.0
    result = 0.0
    for t in data:
        sum1 += t
    if len(data)>0:
        sum1 /= len(data)
    return sum1

"""
对原始信号进行降采样返回两个参数
1.返回outputdata,表示每隔times取原始信号的一个值
2.返回sum_array,从index为0开始，累加times个原始信号作为一个新的值加入sum_array中，
"""
def ChangeHz_Std(srcfile = "",times=32):
    # WIDTH = 20  # 20/500 = 0.04 s, 500/25 * 60 = 1200 bpm
    # WIDTH_HALF = int(WIDTH / 2)
    # last_20_width = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    src_file = open(srcfile, "rb")
    src_data = src_file.read()
    in_data_abs = bytearray()
    #转绝对值 ---128。求取原始数据与128之间的绝对值，并存在in_data_abs中
    for ti in range(0, len(src_data)):
        in_data_abs.append(get_data(src_data[ti]))

    #每32获取一个值
    outputdata = in_data_abs[::times]
    # in_data = bytearray()
    sum_array = []
    # sumarray_str = ""
    #从index为0开始，每32个点进行累加，并将每次的累加值存入sum_array中
    for ti in range(0,len(in_data_abs)-times*4,times):
        temp = 0
        for tj in range(0,times*4):
            temp += in_data_abs[ti + tj]
        sum_array.append(temp)
        # sumarray_str+= struct.pack("i",int(temp,2))
    fix_array = sum_array
    src_file.close()
    
    # print(len(outputdata))
    # print(len(sum_array))
    # print(len(fix_array))
    # return  outputdata,fix_array
    return  outputdata,sum_array

def srcdata_process(filename, times):
    indata1file = open("data1.pkl", "wb")
    indata2file = open("data2.pkl", "wb")
    indata1, indata2 = ChangeHz_Std(filename, times)
    pickle.dump(indata1, indata1file, -1)
    pickle.dump(indata2, indata2file, -1)
    indata1file.close()
    indata2file.close()


def corr1( in_data1, in_data2, dif):
    """
    幅度自相关
    :param in_data1: 
    :param in_data2: 
    :return: 
    """
   
    corr_data1 = []
    corr_data2 = []

    for j in range(0, dif):
        sum1 = 0.0
        sum2 = 0.0

        for i in range(0, dif):
            #            sum1 += math.sqrt(in_data1[i+start_index] *  in_data1[j+start_index+i])
            #            sum2 += math.sqrt(in_data2[i+start_index] * in_data2[j+start_index + i])
            if (j + i) < dif:
                sum1 += abs(in_data1[i] - in_data1[j + i])
                sum2 += abs(in_data2[i] - in_data2[j + i])
            else:
                break


        corr_data1.append(sum1)
        corr_data2.append(sum2)

    div1 = numpy.mean(corr_data1)/100  #
    div2 = numpy.mean(corr_data2)/100
    # print("corr1_data1_length:"+str(len(corr_data1)))
    for i in range(0,len(corr_data1)):
        # print("corrdata1:"+str(i)+","+str(corr_data1[i]))
        res1 = math.isnan(float(corr_data1[i]))
        res2 = math.isnan(float(corr_data2[i]))
        if div1!=0 and not res1 and not res2:
            corr_data1[i] = int(corr_data1[i]/div1)
            corr_data2[i] = int(corr_data2[i]/div2)
        else:
            continue


    return corr_data1, corr_data2

def amdf_curve(data1, data2):
    # end_posi = int(len(Infiledata.in_data2) - 2 * CORR_LEN - CORR_STEP)
    y1_array = []
    y2_array = []

    for getfhr_i in range(0, len(data2), CORR_STEP):
        startindex = getfhr_i
        if startindex <= (len(data2) - 2*CORR_LEN):
            endindex = getfhr_i + CORR_LEN * 2
        else:
            endindex = len(data2) - 1
        dif = endindex - startindex
        # logger.info("start and end of ydata2 to calc fhr:"+ str(startindex)+","+str(endindex))
        in_data1 = data1[startindex:endindex]
        in_data2 = data2[startindex:endindex]
        
        
        avg = get_avg(in_data2)
        fix_num = int(avg / 30)
        for i in range(0, dif):
            in_data2[i] = int(in_data2[i] / fix_num)

        y1, y2 = corr1(in_data1, in_data2, dif)
        y1_array.extend(y1)
        y2_array.extend(y2)
    
    return y1_array, y2_array

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
              _files.append(path)
    return _dir


if __name__ == "__main__":

    # filename = '19826_161010104449'
    # filespath = ("E:/LU/fhr_analyse/completedoc/{0}/{1}.adpcm").format(filename,filename)
    filename = 'E:/LU/fhr_analyse/amdfcsvdata/2970_160707094518.csv'
 
    fileid = filename.split('/')
    datafromfile = pd.read_csv(filename)
    
    import time
    time0 = time.time()
    for i in range(0, 733575, 400):
        time1 = time.time()
        x_axis = []
        y_axis = []
        if i+400<=733575:
            for j in range(i, i+400):
                x_axis.append(datafromfile.iloc[j][0]/100)
                y_axis.append(datafromfile.iloc[j][1])
        else:
            for j in range(i, 733575):
                x_axis.append(datafromfile.iloc[j][0]/100)
                y_axis.append(datafromfile.iloc[j][1])  
        plt.figure(num=1,figsize=(15,5))
        plt.plot(x_axis, y_axis)
        plt.ylim(0, 280)
        plt.savefig("E:/LU/fhr_analyse/2970_160707094518-400/{0}-{1}.svg".format(i,i+399))
        plt.close()
        time2 = time.time()
        print('the {0} th of the time spend '.format(int(i/400+1)) + str(round((time2-time1))))
        
    print("total time:" + str(time.time()-time0))
    # print(len(datafromfile))
    
    # for i in range(5000, 5120):
    #     x_axis.append(datafromfile.iloc[i][0]/100)
    #     y_axis.append(datafromfile.iloc[i][1])
    # import time
    # time1 = time.time() 
    # # print(time1)
    # plt.figure()
    # plt.plot(x_axis, y_axis)
    # print(time.time()- time1)
    # plt.savefig('E:/LU/fhr_analyse/{0}.svg'.format(fileid[-1]))
    # plt.close()



