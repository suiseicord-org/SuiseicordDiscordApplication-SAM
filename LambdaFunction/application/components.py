#!python3.9
from application.enums import (
    ComponentType,
    ButtonStyle,
)

from application.commands import (
    Commands as CommandsName,
    SlashCommand as SlashCommandName,
    SlashChannelCommand as SlashChannelCommandName,
    HappiCommand as HappiCOmmandName,
    HappiAnnounceLanguage
)

class CustomID:
    start_send: str = f'{CommandsName.start}-{SlashCommandName.send}-' + '{sub_command}-{target}'
    modal_send: str = f'{CommandsName.modal}-{SlashCommandName.send}-' + '{sub_command}-{target}'
    textinput_send: str = f'{CommandsName.textinput}-{SlashCommandName.send}'

    start_channel_topic: str = f'{CommandsName.start}-{SlashChannelCommandName.channel_topic}-' + '{target}'
    modal_channel_topic: str = f'{CommandsName.modal}-{SlashChannelCommandName.channel_topic}-' + '{target}'
    textinput_channel_topic: str = f'{CommandsName.textinput}-{SlashChannelCommandName.channel_topic}'

    start_ban: str = f'{CommandsName.start}-{SlashCommandName.ban}' + '-{count}-{target}-{del_day}-{dm}'
    cancel_ban: str = f'{CommandsName.cancel}-{SlashCommandName.ban}' + '-{count}'
    modal_ban: str = f'{CommandsName.modal}-{SlashCommandName.ban}'
    textinput_ban: str = f'{CommandsName.textinput}-{SlashCommandName.ban}'

    cansell: str = CommandsName.cancel

    # text input custom ids
    text: str = "text"


    #suiseicord happi custom ids
    happi_announce_jp: str = f'{CommandsName.happi}-{HappiCOmmandName.announce}-{HappiAnnounceLanguage.jp}'
    happi_announce_en: str = f'{CommandsName.happi}-{HappiCOmmandName.announce}-{HappiAnnounceLanguage.en}'

    class PermissionType:
        command = 'cmd'
        user    = 'usr'
        all     = 'all'

    @classmethod
    def set_permission(cls, target: str, _type: str, _id: int) -> str:
        return target + f'-{_type}-{str(_id)}'

class Button:
    
    @classmethod
    def cansell(cls, permission_type: str, permission_id: int) -> dict:
        return {
            "type" : ComponentType.button.value,
            "style" : ButtonStyle.danger.value,
            "label" : "Cancel (中止)",
            "custom_id" : CustomID.set_permission(
                CustomID.cansell,
                permission_type,
                permission_id
            ) 
        }
