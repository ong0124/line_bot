from linebot.models import FlexSendMessage

def no_booking_flex_message(liff_url: str) -> FlexSendMessage:
    return FlexSendMessage(
        alt_text="【未找到預約】",
        contents={
            "type": "bubble",
            "size": "mega",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/oBm5fkC.png",
                "size": "full",
                "aspectRatio": "20:10",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "目前沒有查詢到您的預約",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "color": "#757575",
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": "點擊下面按鈕安排一下～",
                        "size": "md",
                        "align": "center",
                        "color": "#666666",
                        "margin": "md"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "立即預約",
                            "uri": liff_url
                        },
                        "style": "primary",
                        "color": "#4CAF50"
                    }
                ],
                "spacing": "sm"
            }
        }
    )
