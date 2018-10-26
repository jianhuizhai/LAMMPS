import os 
class  SearchFile(object): 
    def __init__(self,path='.'): 
        self._path=path 
        self.abspath=os.path.abspath(self._path) # 默认当前目录 
        
    def findfile(self,keyword,root): 
        filelist=[] 
        for root,dirs,files in os.walk(root): 
            for name in files: fitfile=filelist.append(os.path.join(root, name)) 
            #print(fitfile) 
            # print(os.path.join(root, name)) 
        #print(filelist) 
        # print('...........................................') 
        for i in filelist: 
            if os.path.isfile(i): 
                #print(i) 
                if keyword in os.path.split(i)[1]: 
                    # print('yes!',i) # 绝对路径
                    return i
                #else: 
                    #print('......no keyword!') 
    def __call__(self): 
        while True: 
            workpath=input('Do you want to work under the current folder? Y/N:') 
            if(workpath == ''): 
                break 
            if workpath=='y' or workpath=='Y': 
                root=self.abspath # 把当前工作目录作为工作目录 
                print('当前工作目录：',root) 
                dirlist=os.listdir() # 列出工作目录下的文件和目录 
                print(dirlist) 
            else: 
                root=input('please enter the working directory:') 
                print('当前工作目录：',root) 
            keyword=input('the keyword you want to find:') 
            if(keyword==''): 
                break 
            self.findfile(keyword,root) # 查找带指定字符的文件
            
if __name__ == '__main__':
    search = SearchFile()
    search()