import json
import pycurl
import sys
import urllib2
import wave

from pydub import AudioSegment

sys.path.append('/Users/agenthun/Android/')


# from pydub import AudioSegment

## get access token by api key & secret key

class VoiceService:
    def __init__(self):
        self.buff = ''
        self.isOk = False

    def get_token(self):
        apiKey = "neeyG1mx11OttAiAlR0AuAgG"
        secretKey = "f9441312152038555ae41fa12b7f4130"

        auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;

        res = urllib2.urlopen(auth_url)
        json_data = res.read()
        return json.loads(json_data)['access_token']

    def dump_res(self, buf):
        self.isOk = True
        self.buff = buf
        print buf

    ## post audio to server
    def use_cloud(self, sourcefile_path, token):
        # sound = AudioSegment.from_mp3("big.mp3")
        # sound.export("/output", format="wav")
        fp = wave.open(sourcefile_path, 'rb')
        nf = fp.getnframes()
        f_len = nf * 2
        audio_data = fp.readframes(nf)

        cuid = "xxxxxxxxxx"  # my xiaomi phone MAC
        srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token
        http_header = [
            'Content-Type: audio/pcm; rate=8000',
            'Content-Length: %d' % f_len
        ]

        c = pycurl.Curl()
        c.setopt(pycurl.URL, str(srv_url))  # curl doesn't support unicode
        # c.setopt(c.RETURNTRANSFER, 1)
        c.setopt(c.HTTPHEADER, http_header)  # must be list, not dict
        c.setopt(c.POST, 1)
        c.setopt(c.CONNECTTIMEOUT, 30)
        c.setopt(c.TIMEOUT, 30)
        c.setopt(c.WRITEFUNCTION, self.dump_res)
        c.setopt(c.POSTFIELDS, audio_data)
        c.setopt(c.POSTFIELDSIZE, f_len)
        c.perform()  # pycurl.perform() has no return val

    def voicepro(self, sourcefile_path):
        token = self.get_token()
        self.use_cloud(sourcefile_path, token)


def getOutput(sourcefile_path, targetfile_path):
    song = AudioSegment.from_mp3(sourcefile_path).export(targetfile_path, format="wav")
    voiceService = VoiceService()
    voiceService.voicepro(targetfile_path)
    while True:
        if voiceService.isOk:
            usage = json.loads(voiceService.buff)
            result = usage['result']
            return result


print getOutput('/Users/agenthun/Documents/Python save/jiang/voice/testmap.mp3',
                '/Users/agenthun/Documents/Python save/jiang/voice/test.wav')
