#!python3.9



from ctypes.wintypes import tagRECT


class Commands:
    cancel = "cansell"
    start = "start"
    modal = "modal"
    textinput = "textinput"
    form = "form"
    
    #suiseicord happi
    happi = "happi"

class SlashCommand:
    send    = "send"
    getlog  = "getlog"
    user    = "user"
    thread  = "thread"
    channel = "channel"
    ban     = "ban"

class SendCommand:
    dm = "dm"
    channel = "channel"
    happi = "happi_announce"

class SendCommandOption:
    target          = 'target'
    attachments     = 'attachments'

class UserCommand:
    id      = 'id'
    mention = 'mention'

class UserCommandOption:
    target  = 'target'

class GetlogCommand:
    dm = "dm"

class GetlogCommandOption:
    target = 'target'

class ThreadCommand:
    create = "create"

class ChannelCommand:
    topic  = "topic"
    channel_topic = "channeltopic"

class ChannelCommandOption:
    channel = "channel"

class TextinputSubCommand:
    send = "send"
    # suiseicord happi
    happi = "happi"

class FormCategory:
    vsong_award = "vsongaward"


class VSongAwardYear:
    vsa_2022 = "2022"

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