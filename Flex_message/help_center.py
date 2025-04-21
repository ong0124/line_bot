from linebot.models import FlexSendMessage

def help_center_flex(user_name, user_id):
    print(f"用户昵称2：{user_name} 用户ID：{user_id} 点击了帮助按钮")
    return FlexSendMessage(
        alt_text="【幫助中心】",
        contents = {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "幫助中心",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "如果您遇到任何問題，可以參考以下幫助信息。",
                        "wrap": True,
                        "size": "sm",
                        "color": "#999999",
                        "margin": "lg",
                        "align": "start"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "paddingAll": "none",
                "paddingStart": "lg",
                "paddingEnd": "lg",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "margin": "sm",
                        "action": {
                            "type": "message",
                            "label": "如何預約接駁車？",
                            "text": "如何預約接駁車？"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "margin": "sm",
                        "action": {
                            "type": "message",
                            "label": "聯繫客服",
                            "text": "聯繫客服"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "margin": "sm",
                        "action": {
                            "type": "message",
                            "label": "操作指南",
                            "text": "如何修改我的預約信息？"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "margin": "sm",
                        "action": {
                            "type": "message",
                            "label": "服務時間",
                            "text": "工作時間"
                        }
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "margin": "sm",
                        "action": {
                            "type": "uri",
                            "label": "反饋和建議",
                            "uri": "https://line.me/"
                        }
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "我們的客服團隊工作時間為每天",
                        "size": "sm",
                        "wrap": True,
                        "color": "#999999",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "9:00 AM - 6:00 PM",
                        "size": "sm",
                        "wrap": True,
                        "color": "#999999",
                        "align": "center"
                    }
                ]
            }
        }
    )
