#!python3.9

class Commands:
    cancel = 'cansell'
    start = 'start'
    modal = 'modal'
    textinput = 'textinput'
    form = 'form'
    role = 'role'
    
    #suiseicord happi
    happi = 'happi'

# SlashCommands
class SlashCommand:
    send    = 'send'
    getlog  = 'getlog'
    user    = 'user'
    thread  = 'thread'
    channel = 'channel'
    ban     = 'ban'

    test    = 'test'

class SendCommand:
    dm = 'dm'
    channel = 'channel'
    happi = 'happi_announce'

class SendCommandOption:
    target          = 'target'
    attachments     = 'attachments'

class UserCommand:
    id      = 'id'
    mention = 'mention'

class UserCommandOption:
    target  = 'target'

class BanCommand:
    id      = 'id'
    mention = 'mention'

class BanCommandOption:
    target = 'target'
    reason = 'reason'
    delete_message_days = 'delete-message-days'
    custom_reason = 'custom-reason'
    dm = 'dm'
    dm_attachments = 'dm_attachments'
    attachments = 'attachments'
    accept_count = 'accept-count'
    cancel_count = 'cancel-count'
    dm_text = 'dm-text'
    mentions = 'mentions'

    accept_title = '必要承認人数'
    cancel_title = '必要中止人数'

class GetlogCommand:
    dm = 'dm'

class GetlogCommandOption:
    target = 'target'

class ThreadCommand:
    create = 'create'

class ChannelCommand:
    topic  = 'topic'
    channel_topic = 'channeltopic'

class ChannelCommandOption:
    channel = 'channel'

# Message Command
class MessageCommand:
    save   = 'save'
    report = 'report'

# Text Input Command
class TextinputSubCommand:
    send = 'send'
    channel_topic = 'channeltopic'
    ban = 'ban'
    # suiseicord happi
    happi = 'happi'

class FormCategory:
    vsong_award = 'vsongaward'

class RoleCommand:
    add = 'add'
    update = 'update'
    button = 'button'
    select = 'select'


class VSongAwardYear:
    vsa_2022 = '2022'

# Suiseicord Happi
class HappiCommand:
    announce = 'announce'
    report   = 'payreport'
    check    = 'paycheck'

class HappiPayreportAction:
    bank        = 'bank'
    paypal_jp   = 'paypal_jp'
    paypal_en   = 'paypal_en'

class HappiAnnounceLanguage:
    jp = 'jp'
    en = 'en'