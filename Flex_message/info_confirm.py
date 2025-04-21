from linebot.models import FlexSendMessage

def booking_confirm_flex(date_with_weekday: str, time_range: str, location: str, liff_url: str) -> FlexSendMessage:
    return FlexSendMessage(
        alt_text="【預約信息】",
        contents={
            "type": "bubble",
            "size": "kilo",
            "hero": {
                "type": "image",
                "url": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1b/4a/d3/fb/caption.jpg?w=500&h=400&s=1",
                "size": "full",
                "aspectRatio": "20:9",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "預約確認",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "color": "#1DB446",
                        "margin": "sm"
                    },
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": "#EEEEEE"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "md",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [{"type": "text", "text": "📅", "size": "sm", "align": "center"}],
                                        "width": "40px"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {"type": "text", "text": "接駁日期", "color": "#888888", "size": "sm"},
                                            {"type": "text", "text": date_with_weekday, "color": "#333333", "weight": "bold", "size": "md", "margin": "sm"}
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [{"type": "text", "text": "⏰", "size": "sm", "align": "center"}],
                                        "width": "40px"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {"type": "text", "text": "接駁時間", "color": "#888888", "size": "sm"},
                                            {"type": "text", "text": time_range, "color": "#333333", "weight": "bold", "size": "md", "margin": "sm"}
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [{"type": "text", "text": "📍", "size": "sm", "align": "center"}],
                                        "width": "40px"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {"type": "text", "text": "接駁地點", "color": "#888888", "size": "sm"},
                                            {"type": "text", "text": location, "color": "#333333", "weight": "bold", "size": "md", "margin": "sm", "wrap": True}
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": "#EEEEEE"
                    },
                    {
                        "type": "text",
                        "text": "我們會提前30分鐘到達指定地點等候",
                        "color": "#888888",
                        "size": "xs",
                        "align": "center",
                        "margin": "lg",
                        "wrap": True
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
                            "label": "查看詳情 & 修改預約",
                            "uri": liff_url
                        },
                        "style": "link",
                        "height": "sm",
                        "margin": "sm"
                    }
                ],
                "spacing": "sm"
            },
            "styles": {
                "body": {"backgroundColor": "#FFFFFF"},
                "footer": {"backgroundColor": "#F9F9F9", "separator": True}
            }
        }
    )
