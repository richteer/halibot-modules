from module import XMPPModule
import re, requests

class Link(XMPPModule):
   
    def init(self):
        self.addrReg = re.compile('.*(http[s]?://.*)+')
        self.titleReg = re.compile('.*<title>(.*)</title>')

    def handleMessage(self, msg):
        obj = self.addrReg.match(msg['body'])

        if obj:
            addr = obj.group(1)
            webpage = requests.get(addr).content
            title = self.titleReg.match(str(webpage)).group(1).rstrip().lstrip()
            self.xmpp.reply(msg, "Website: " + title)
