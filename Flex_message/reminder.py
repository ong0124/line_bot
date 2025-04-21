from linebot.models import FlexSendMessage
def reminder_flex(location: str, date_with_weekday: str, time_range: str, liff_url: str) -> FlexSendMessage:
    flex_message = {
        "type": "bubble",
        "alt_text": "⏰ 接駁服務提醒",
        "contents": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "⏰ 接駁服務提醒",
                    "color": "#308EBD",
                    "weight": "bold"
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "text",
                    "text": "接駁服務",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "接駁地點:",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": location,
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "日期：",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": date_with_weekday,
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "時間：",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": time_range,
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        }
                    ]
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
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "查看預約的預訂",
                        "uri": liff_url
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "height": "md",
                    "action": {
                        "type": "message",
                        "label": "回復： 我收到提醒了",
                        "text": "我收到提醒了"
                    }
                },
                {
                    "type": "text",
                    "text": "Powered by 上車巴",
                    "position": "relative",
                    "align": "center",
                    "size": "xxs",
                    "color": "#B3B3B3",
                    "margin": "md"
                }
            ],
            "paddingAll": "xl"
        }
    }

    return FlexSendMessage(alt_text="⏰ 接駁服務提醒", contents=flex_message)
