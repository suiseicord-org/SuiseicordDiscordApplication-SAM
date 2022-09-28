#!python3.9



from ctypes.wintypes import tagRECT


class Commands:
    cancel = "cansell"
    start = "start"
    modal = "modal"
    textinput = "textinput"
    
    #suiseicord happi
    happi = "happi"

class SlashCommand:
    send = "send"
    getlog = "getlog"
    user = "user"

class SendCommand:
    dm = "dm"
    channel = "channel"
    happi = "happi_announce"

class SendCommandOption:
    target          = 'target'
    attachments     = 'attachments'

class GetlogCommand:
    dm = "dm"

class GetlogCommandOption:
    target = 'target'

class TextinputSubCommand:
    send = "send"
    # suiseicord happi
    happi = "happi"

class HappiCommand:
    announce = "announce"
    report   = "payreport"
    check    = "paycheck"

class HappiPayreportAction:
    bank        = "bank"
    paypal_jp   = "paypal_jp"
    paypal_en   = "paypal_en"

class HappiAnnounceLanguage:
    jp = "jp"
    en = "en"