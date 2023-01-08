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

class SlashSendCommand:
    dm = 'dm'
    channel = 'channel'
    happi = 'happi_announce'

class SlashSendCommandOption:
    target          = 'target'
    attachments     = 'attachments'

class SlashUserCommand:
    id      = 'id'
    mention = 'mention'

class SlashUserCommandOption:
    target  = 'target'

class SlashBanCommand:
    id      = 'id'
    mention = 'mention'

class SlashBanCommandOption:
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

class SlashGetlogCommand:
    dm = 'dm'

class SlashGetlogCommandOption:
    target = 'target'

class SlashThreadCommand:
    create = 'create'

class SlashChannelCommand:
    topic  = 'topic'
    channel_topic = 'channeltopic'

class SlashChannelCommandOption:
    channel = 'channel'

# Message Command
class MessageCommand:
    save   = 'save'
    report = 'report'

class UserCommand:
    info   = 'user-info'

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