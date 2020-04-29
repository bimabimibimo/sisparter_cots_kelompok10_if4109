import os
import requests
import threading
import urllib.request, urllib.error, urllib.parse
import time

url = "https://apod.nasa.gov/apod/image/1901/LOmbradellaTerraFinazzi.jpg"


def buildRange(value, numsplits):
    lst = []
    #mensplit variable value berdasarkan numsplits
    for i in range(numsplits):
        if i == 0:
            lst.append('%s-%s' % (i, int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
        else:
            lst.append('%s-%s' % (int(round(1 + i * value/(numsplits*1.0),0)), int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
    return lst

class SplitBufferThreads(threading.Thread):
    """ Splits the buffer to ny number of threads
        thereby, concurrently downloading through
        ny number of threads.
    """
    #menginisialisasi kelas dengan url dan byterange
    def __init__(self, url, byteRange):
        super(SplitBufferThreads, self).__init__()
        self.__url = url
        self.__byteRange = byteRange
        self.req = None

    #mrngakses alamat url yang diberikan
    def run(self):
        self.req = urllib.request.Request(self.__url,  headers={'Range': 'bytes=%s' % self.__byteRange})
    
    #membuka alamat url yang sudah diberikan
    def getFileData(self):
        return urllib.request.urlopen(self.req).read()


def main(url=None, splitBy=3):
    #men set waktu mulai
    start_time = time.time()
    #jika bukan url maka masukkan lagi
    if not url:
        print("Please Enter some url to begin download.")
        return

    #untuk mengambil nama filenya, dengan cara mengambil indeks terakhir dari url yang di split berdasarkan karakter '/'
    fileName = url.split('/')[-1]
    #cek size dari file di url
    sizeInBytes = requests.head(url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)
    print("%s bytes to download." % sizeInBytes)
    if not sizeInBytes:
        print("Size cannot be determined.")
        return

    #memasukkan data yang sudah diambil ke dalam list
    dataLst = []
    for idx in range(splitBy):
        byteRange = buildRange(int(sizeInBytes), splitBy)[idx]
        bufTh = SplitBufferThreads(url, byteRange)
        bufTh.start()
        bufTh.join()
        dataLst.append(bufTh.getFileData())

    content = b''.join(dataLst)
    #jika nama file yang ada di direktori sudah ada maka file lama akan di remove terlebih dahulu
    #write file di direktori
    if dataLst:
        if os.path.exists(fileName):
            os.remove(fileName)
        #print waktu proses download
        print("--- %s seconds ---" % str(time.time() - start_time))
        with open(fileName, 'wb') as fh:
            fh.write(content)
        print("Finished Writing file %s" % fileName)
#main program
if __name__ == '__main__':
    main(url)