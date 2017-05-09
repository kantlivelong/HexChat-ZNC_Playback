import hexchat
import random
import time

__module_name__ = 'ZNC_Playback'
__module_author__ = 'kantlivelong'
__module_version__ = '1.0'
__module_description__ = 'Provides support for the znc.in/playback module'

servers = {}

def caplst_cb(word, word_eol, userdata):
    if "znc.in/playback" in word[1]:
        hexchat.command("cap req znc.in/playback")

def capack_cb(word, word_eol, userdata):
    if "znc.in/playback" in word[1]:
    hexchat.emit_print("Capability Request", "znc.in/playback")
    id = hexchat.get_prefs("id")
    try:
        test = servers[id]
    except:
        servers[id] = 0

def endmotd_cb(word, word_eol, userdata):
    id = hexchat.get_prefs("id")
    timestamp = servers[id]
    hexchat.command("znc *playback play * " + str(timestamp))

def clsctxt_cb(word, word_eol, userdata):
    id = hexchat.get_prefs("id")
    timestamp = servers[id]
    
    try:
        ctx_type = ''
        list = hexchat.get_list('channels')
        for i in list:
            if i.channel == hexchat.get_info('channel'):
                ctx_type = i.type
        if ctx_type == '':
            return
    except:
        return
    
def opnctxt_cb(word, word_eol, userdata):
    id = hexchat.get_prefs("id")
    
    try:
        timestamp = servers[id]
    except:
        return
    
    if timestamp == 0:
        return

    try:
        list = hexchat.get_list('channels')
        for i in list:
            if i.channel == hexchat.get_info('channel'):
                ctx_type = i.type
        if ctx_type == '':
            return
    except:
        return

    if ctx_type == 3: # Dialog
        chan = hexchat.get_info('channel')
        hexchat.command('znc *playback play ' + chan + ' ' + str(timestamp))

def privmsg_cb(word, word_eol, userdata, attrs):
    id = hexchat.get_prefs("id")
    servers[id] = time.time()


hexchat.hook_print('Capability List', caplst_cb)
hexchat.hook_print('Capability Acknowledgement', capack_cb)
hexchat.hook_server('376', endmotd_cb)
hexchat.hook_print('Close Context', clsctxt_cb)
hexchat.hook_print('Open Context', opnctxt_cb)
hexchat.hook_server_attrs('PRIVMSG', privmsg_cb)
