from linebot.models import FlexSendMessage

def get_service_flex(liff_url: str) -> FlexSendMessage:
    flex_message = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://i.imgur.com/TFr5Ndf.png",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": liff_url
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "上車巴",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "separator",
                    "margin": "xs"
                },
                {
                    "type": "text",
                    "text": "接駁服務",
                    "align": "center",
                    "size": "sm",
                    "margin": "sm",
                    "color": "#ACACAC"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "點擊使用",
                        "uri": liff_url
                    }
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": "Powered by 上車巴",
                    "size": "xxs",
                    "align": "center"
                }
            ],
            "flex": 0
        }
    }
    return FlexSendMessage(alt_text="這是接駁服務", contents=flex_message)
