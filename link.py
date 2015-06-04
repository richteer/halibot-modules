from module import XMPPModule
import halutils
import re, requests
 
class Link(XMPPModule):
    
    def handleMessage(self, msg):
        obj = re.match('.*(http[s]?://.*)+', msg['body'])
 
        if obj:
            addr = obj.group(1)
            webpage = requests.get(addr).content
            title = re.match('.*<title>(.*)</title>', str(webpage)).group(1).rstrip().lstrip()
            self.xmpp.reply(msg, "Website: " + title) 
