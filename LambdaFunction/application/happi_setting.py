#!python3.9
from .mytypes.snowflake import Snowflake

class HappiSetting:
    httpPath = "/Discord-SAM-SuiseiCordHap-SuiseiHappiApplicationCo-MLggnTqIZqJT"
    
    class Channel:
        payreport: Snowflake = 983236396141670420 # BOT TEST
    
    class Form:
        jpform = {
            "url" : "https://docs.google.com/forms/d/e/1FAIpQLSffqZ9121Y1_XILnLGMr824Fz8kp2bGdPWsjgCRvIz9Y5wNxw/viewform",
            "entrys" : {
                "user_id" : "767747983",
                "name"    : "806591022"
            }
        }
        enform = {
            "url" : "https://docs.google.com/forms/d/e/1FAIpQLScwjaLFK2lAHNs9akXXaGa_trqWlGVt0P0bWX_SLMCa8RDF-A/viewform",
            "entrys" : {
                "user_id" : "804891122",
                "name"    : "881507775"
            }
        }

        jplabel = "申し込みフォーム"
        enlabel = "Form Link"
