from PIL import Image
from multiprocessing import Process
import histogram as htg
import aHash as ah
import pHash as ph
import dHash as dh
import os

def imgsearch(file_name):
    flag=0
    tmp=0
    name=""
    #filenames=os.listdir(r"dataset")
    # read image files
    img1 = Image.open(file_name)
    img1_htg = htg.regularizeImage(img1)
    hg1 = img1_htg.histogram()
    '''for i in os.listdir("dataset"):
        for filename in os.listdir("dataset"+"/"+i):
            img2 = Image.open("dataset"+"/"+i+"/"+filename)
            img2_htg = htg.regularizeImage(img2)
            hg2 = img2_htg.histogram()
            sub_thread = Process(target=htg.drawHistogram, args=(hg1, hg2,))
            sub_thread.start()
            res=htg.calMultipleHistogramSimilarity(img1_htg, img2_htg)*64+ah.calaHashSimilarity(img1, img2)+ph.calpHashSimilarity(img1, img2)+dh.caldHashSimilarity(img1, img2)
            #print(res)
            if(res<160):
                flag+=1
                if(flag>15):
                    flag=0
                    break
            if(res>200.0):
                name=filename
                return(name[:-4])
            elif(res>tmp):
                tmp=res
                name=filename
            else:
                continue
    return(name[:4])'''   
    for filepath,dirnames,filenames in os.walk(r'dataset'):
        for filename in filenames:
            img2 = Image.open(filepath+"/"+filename)
            img2_htg = htg.regularizeImage(img2)
            hg2 = img2_htg.histogram()
            sub_thread = Process(target=htg.drawHistogram, args=(hg1, hg2,))
            sub_thread.start()
            res=htg.calMultipleHistogramSimilarity(img1_htg, img2_htg)*64+ah.calaHashSimilarity(img1, img2)+ph.calpHashSimilarity(img1, img2)+dh.caldHashSimilarity(img1, img2)
            #print(res)
            if(res>200.0):
                name=filename
                return(name[:-4])
            elif(res>tmp):
                tmp=res
                name=filename
            else:
                continue
    #return(name[:-4])
    return(name[:5])        