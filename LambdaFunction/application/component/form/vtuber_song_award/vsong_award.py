#!python3.9
from requests import Response
from ..form import Form

from application.enums import (
    InteractionResponseType,
    ComponentType,
    ButtonStyle
)
from application.enums import (
    MessageFlags
)

class VSongAward(Form):
    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)
        self.mv_entrys: list[str] = []
        self.song_entrys: list[str] = []
        self.mv_titles: list[str] = []
        self.song_titles: list[str] = []
        self.values: list[str] = self._data["values"]
        self.content: str = '生成されたリンクから投票ができます！\n↓↓↓↓'
        self.parse_titles()

    def check(self) -> bool:
        return self.check_permission()

    def run(self) -> None:
        super().run()
        return

    def response(self) -> None:
        self.set_entrys()
        url = self.inputed_url
        if len(url) < 512:
            payload: dict = {
                "type" : InteractionResponseType.channel_message.value,
                "data" : {
                    "flags" : MessageFlags.ephemeral.value,
                    "content" : self.content,
                    "components" : [
                        {
                            "type" : ComponentType.action_row.value,
                            "components" : [
                                {
                                    "type" : ComponentType.button.value,
                                    "style" : ButtonStyle.link.value,
                                    "label" : "投票用リンク (Vote)",
                                    "url" : self.inputed_url
                                }
                            ]
                        }
                    ]
                }
            }
        else:
            self.content += f'\n<{url}>'
            payload: dict = {
                "type" : InteractionResponseType.channel_message.value,
                "data" : {
                    "flags" : MessageFlags.ephemeral.value,
                    "content" : self.content
                }
            }
        r: Response = self.callback(payload)
        return 
    
    def clean(self) -> None:
        return super().clean()
    
    def parse_titles(self):
        for value in self.values:
            _type, title = value.split('-', 1)
            if _type in ('song', 'all'):
                self.song_titles.append(title)
            if _type in ('mv', 'all'):
                self.mv_titles.append(title)
    
    def set_entrys(self):
        n = min(len(self.song_entrys), len(self.song_titles))
        for i in range(n):
            self.entrys[self.song_entrys[i]] = self.song_titles[i]
        n = min(len(self.mv_entrys), len(self.mv_titles))
        for i in range(n):
            self.entrys[self.mv_entrys[i]] = self.mv_titles[i]    