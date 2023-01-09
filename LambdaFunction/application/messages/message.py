#!python3.9
import os

class MessageFile:
    send = "send"

    # SuiseiCord Happi Files
    class SuiseiCordHappi:
        suiseicord_happi = "suiseicord_happi/"
        payreport_response = suiseicord_happi + "payreport_response.txt"
        paycheck_complete = suiseicord_happi + "paycheck_complete.txt"
        announce = suiseicord_happi + "announce.txt"
        guide_jp = suiseicord_happi + "guide-jp.txt"
        guide_en = suiseicord_happi + "guide-en.txt"


def filepath(name: str) -> str:
    return os.path.dirname(__file__) + "/" + name
    