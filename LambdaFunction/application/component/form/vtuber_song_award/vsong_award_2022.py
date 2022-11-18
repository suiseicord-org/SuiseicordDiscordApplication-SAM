#!python3.9

from .vsong_award import VSongAward

class VSongAward2022(VSongAward):
    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)
        self.form_url: str = 'https://docs.google.com/forms/d/e/1FAIpQLSeRD6OyKNOnVDbb2vtktWV1W1sarYj8iM7sDGlPmJW3pMwMSA/viewform'
        self.mv_entrys: list[str] = [
            "1092816918",
            "1912025328",
            "470153951"
        ]
        self.song_entrys: list[str] = [
            "1956970528",
            "563240479",
            "956291487",
            "720971646",
            "866419020"
        ]

    def check(self) -> bool:
        return self.check_permission()

    def run(self) -> None:
        super().run()
        return

    def response(self) -> None:
        super().response()
        return 
    
    def clean(self) -> None:
        return super().clean()