msgid_Qns=0
class Message():
    def __init__(self,userid,mtitle,mbody):
        self.__userid=userid
        self.__mtitle=mtitle
        self.__mbody=mbody
    def getuid(self):
        return self.__userid
    def setmtitle(self,mtitle):
        self.__mtitle=mtitle
    def getmtitle(self):
        return self.__mtitle
    def setmbody(self,mbody):
        self.__mbody=mbody
    def getmbody(self):
        return self.__mbody

class Question(Person):
    def __init__(self,userid,mtitle,mbody):
        super().__init__(userid,mtitle,mbody)
        self.__msgid_Qns+=1
        answers_list=[]

class Answer(Person):
    def __init__(self,userid,mbody):
        super().__init__(userid,mbody)
        self.__ans_id=len(userid.answers_list) + 1
        userid.answers_list.append(mbody)
