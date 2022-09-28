#!python3.9

from .enums import (
    ComponentType,
    ButtonStyle,
)

from .commands import (
    Commands as CommandsName,
    SlashCommand as SlashCommandName,
    HappiCommand as HappiCOmmandName,
    HappiAnnounceLanguage
)

class CustomID:
    start_send: str = f'{CommandsName.start}-{SlashCommandName.send}-' + '{sub_command}-{target}'
    modal_send: str = f'{CommandsName.modal}-{SlashCommandName.send}-' + '{sub_command}-{target}'
    textinput_send: str = f'{CommandsName.textinput}-{SlashCommandName.send}'

    cansell: str = CommandsName.cancel

    # text input custom ids
    text: str = "text"


    #suiseicord happi custom ids
    happi_announce_jp: str = f'{CommandsName.happi}-{HappiCOmmandName.announce}-{HappiAnnounceLanguage.jp}'
    happi_announce_en: str = f'{CommandsName.happi}-{HappiCOmmandName.announce}-{HappiAnnounceLanguage.en}'

class Button:
    cansell: dict = {
        "type" : ComponentType.button.value,
        "style" : ButtonStyle.danger.value,
        "label" : "Cancel (中止)",
        "custom_id" : CustomID.cansell
    }