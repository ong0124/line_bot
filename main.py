import json
import os
import uvicorn
import asyncio
from datetime import datetime, timedelta,date
from fastapi import FastAPI, Request, HTTPException, Header
from linebot import WebhookHandler, LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from linebot.models import QuickReply, QuickReplyButton, MessageAction
from dotenv import load_dotenv
from consql import *

app = FastAPI()

# @app.get("/users")
# def read_users():
#     users = get_all_users()
#     return {"users": users}

@app.get("/booking")
def read_bookings():
    bookings = get_all_bookings()
    return  {"bookings" : bookings }

# 读取环境变量中的 LINE 相关信息
load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

line_bot_api = LineBotApi(ACCESS_TOKEN)
line_handler = WebhookHandler(CHANNEL_SECRET)

async def check_json_periodically():
    while True:
        get_all_bookings()
        await asyncio.sleep(60) 

# 读取白名单（后台管理员） JSON
def load_whitelist():
    try:
        with open("whitelist.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ 找不到 whitelist.json，使用空白名单")
        return {}
    except json.JSONDecodeError:
        print("⚠️ JSON 格式错误")
        return {}

whitelist = load_whitelist()

# 处理用户输入进入后台
def process_user_message(user_id, message_text):
    message_text = message_text.strip().lower()  # 转小写，去除空格
    if user_id in whitelist and message_text == whitelist[user_id].lower():
        return "🚀[後端頁面]https://management.kinmentong.com/"
    else:
        return None
    
@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    """处理 LINE 发送过来的消息"""
    body = await request.body()
    body_str = body.decode('utf-8')
    try:
        line_handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        raise HTTPException(status_code=400, detail="Invalid signature.")
    return "OK"

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    """处理用户发送的消息"""
    user_id = event.source.user_id # 获取用户ID（从event中获取）
    user_message = event.message.text.strip()
 
    profile = line_bot_api.get_profile(user_id) # 调用Line API获取用户资料
    user_name = profile.display_name # 获取客户的名字

    message_text = event.message.text.strip().lower()
    response_text = process_user_message(user_id, message_text)

    quick_reply = QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="訂票", text="我要訂票")),
                QuickReplyButton(action=MessageAction(label="接駁服務", text="我要接駁")),
                QuickReplyButton(action=MessageAction(label="查看預約", text="我的預約")),
                QuickReplyButton(action=MessageAction(label="聯繫客服", text="聯繫客服")),
                QuickReplyButton(action=MessageAction(label="幫助中心", text="幫助中心"))
            ]
        )
    
    if user_id in user_bookings:
        booking_info = user_bookings[user_id]
        
        if isinstance(booking_info, list):
            for booking in booking_info:
                location = booking.get('location', '未知')
                booking_date = booking.get('date', '未知')
                booking_time_str = booking.get('time', '未知')
                # 在這裡處理每一筆預訂
                break  # 如果只想處理第一筆，可以用 break 跳出循環
        else:
            # 如果 booking_info 不是列表，直接處理
            location = booking_info.get('location', '未知')
            booking_date = booking_info.get('date', '未知')
            booking_time_str = booking_info.get('time', '未知')
    else:
        location = '未知'
        booking_date = '未知'
        booking_time_str = '未知'

    #设置提醒功能
    # if user_message.count(" ") >= 2:  # 验证格式 "YYYY-MM-DD HH:MM 地点"
    #     try:
    #         parts = user_message.split(" ", 2)
    #         if len(parts) != 3:
    #             raise ValueError("输入格式错误")
    #         booking_date, booking_time, location = parts  # 解析用户输入
    #         # 验证日期格式
    #         datetime.strptime(booking_date, "%Y-%m-%d")  
    #         # 验证时间格式
    #         booking_time_obj = datetime.strptime(booking_time, "%H:%M").time()
    #         # 保存预订信息
    #         user_bookings[user_id] = {
    #             "date": booking_date,
    #             "time": booking_time_obj.strftime("%H:%M"),
    #             "location": location
    #         }
    #         save_user_bookings()  # 保存数据到 JSON
    #         reply_text = f"✅ 你的提醒時間已設置為 {booking_date} {booking_time} {location}，客服會提前 1 個小時提醒您"
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text), quick_reply=quick_reply)
    #         #后台print
    #         print(f"✅ 用户 {user_id} 预定了 {booking_date} {booking_time} 在 {location} 的提醒")
    #     except ValueError:
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="⚠️ 請輸入正確的日期時間格式（YYYY-MM-DD HH:MM 地点）"), quick_reply=quick_reply)
    
    #input message
    if any(keyword in event.message.text for keyword in ["人工电话", "人工","人工電話","客服电话","客服電話","联系客服","聯繫客服","客服"]):
        flex_message = FlexSendMessage(
            alt_text="【人工電話】",
            contents = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "人工電話",
                            "weight": "bold",
                            "size": "xl",
                            "align": "center"
                        },
                        {
                            "type": "separator",
                            "margin": "md"
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
                                            "text": "在線時間：",
                                            "color": "#aaaaaa",
                                            "size": "sm",
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": "上午 9:00 至晚上 6:00（北京時間）",
                                            "wrap": True,
                                            "color": "#666666",
                                            "size": "sm",
                                            "flex": 5,
                                            "align": "start"
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
                                            "text": "☎️電話：",
                                            "color": "#aaaaaa",
                                            "size": "sm",
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "wrap": True,
                                            "color": "#1981E9",
                                            "size": "sm",
                                            "flex": 5,
                                            "align": "start",
                                            "text": "2222-222-222",
                                            "decoration": "underline"
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
                                            "text": "如需幫助，請在此時間段內聯繫我們，我們將竭誠為您服務",
                                            "wrap": True,
                                            "color": "#666666",
                                            "size": "sm",
                                            "flex": 5,
                                            "align": "center"
                                        }
                                    ]
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
                            "style": "secondary",
                            "height": "sm",
                            "action": {
                                "type": "uri",
                                "label": "呼叫",
                                "altUri": {
                                    "desktop": "https://line.me/"
                                },
                                "uri": "tel:2222-222-222"
                            }
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [],
                            "margin": "sm"
                        }
                    ],
                    "flex": 0
                }
            }
        )
        line_bot_api.reply_message(event.reply_token,flex_message)
    
    elif response_text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_text, quick_reply=quick_reply))

    elif any(keyword in event.message.text for keyword in ["客服工作時間", "客服工作时间","工作時間","工作时间"]):
        reply_text = "🖥️ 我們的客服團隊在線時間為每天上午 9:00 至晚上 6:00（北京時間）。如需幫助，請在此時間段內聯繫我們，我們將竭誠為您服務"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text, quick_reply=quick_reply))

    elif any(keyword in event.message.text for keyword in ["帮助", "幫助"]):
        print(f"用户昵称：{user_name} 用户ID：{user_id} 点击了帮助按钮")
        flex_message = FlexSendMessage(
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
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif "旅行助手" in user_message:
        reply_text = "如果您需要幫助，可以告訴我們您遇到的問題，我們會儘力協助您。☀️"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text, quick_reply=quick_reply))
    elif any(keyword in event.message.text for keyword in ["你好", "hello", "您好", "哈喽", "Hi","Hello","hi"]):
        reply_text = f"您好，{user_name}，歡迎使用我們金門通接駁服務！感謝您的選擇，如果您有任何問題或需要幫助，請隨時聯繫我們，我們將竭誠為您服務😊"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text, quick_reply=quick_reply))
    elif "我收到提醒了" in user_message:
        reply_text = "感謝您的確認！如果有其他問題，隨時告訴我😊"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text,quick_reply=quick_reply))
        print(f"✅ 用户 {user_name} 用户ID：{user_id} 确认收到了提醒")

    elif any(keyword in event.message.text for keyword in ["测试", "測試"]):
        print(f'⚙️用户ID: {user_id} , 用户昵称: {user_name}')
        reply_text = "請發送提醒時間（格式：YYYY-MM-DD HH:MM 地点）如：2025-07-22 22:22 國際機場 / 2022-02-22 22:22 迪斯尼樂園。客服會提前 1 個小時提醒您！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text, quick_reply=quick_reply))

    elif any(keyword in event.message.text for keyword in ["我的预约", "我的預約"]):
     # 定义Flex消息
        liff_url = "https://liff.line.me/2006997627-KaPeq5n1"

        print(f"用户昵称：{user_name} 用户ID：{user_id} 点击了我的预约按钮")

     # 获取星期几的中文名称
     # 检查预约信息是否完整
        if not booking_date or booking_date == '未知' or not booking_time_str or booking_time_str == '未知' or not location or location == '未知':
            no_booking_flex = FlexSendMessage(
            alt_text="【未找到預約】",
            contents={
                "type": "bubble",
                "size": "mega",
                "hero": {
                    "type": "image",
                    "url": "https://img2.woyaogexing.com/2022/01/20/80ebbd0faa71430cb1e471e22eb63fea!400x400.jpeg",  # 这里替换成你的可爱表情包图片 URL
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
                            "color": "#4CAF50"  # 绿色
                        }
                    ],
                    "spacing": "sm"
                }
            }
        )

            line_bot_api.reply_message(event.reply_token, no_booking_flex)
            return  # 直接返回，不发送预约详情
        if isinstance(booking_date, str):
            try:
                booking_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
            except ValueError:
                # 處理無效日期格式
                pass

        if isinstance(booking_date, date):
            booking_date_str = booking_date.strftime("%Y-%m-%d")
            # 预约信息完整，继续处理日期和时间
            try:
                booking_datetime = datetime.strptime(booking_date_str, "%Y-%m-%d")
                weekday_num = booking_datetime.weekday()
                weekday_chinese = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}.get(weekday_num, "")
                date_with_weekday = f"{booking_date}({weekday_chinese})"
            except ValueError:
                date_with_weekday = '日期格式错误'

            try:
                booking_time = datetime.strptime(booking_time_str, "%H:%M").time()
                end_time = (datetime.combine(datetime.today(), booking_time) + timedelta(minutes=30)).time()
                time_range = f"{booking_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
            except ValueError as e:
                time_range = f'日期格式错误: {str(e)}'
        
        flex_message = FlexSendMessage(
            alt_text="【預約信息】",
                contents = {
                            "type": "bubble",
                            "size": "kilo",  # 使用更大的尺寸
                            "hero": {
                                "type": "image",
                                "url": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1b/4a/d3/fb/caption.jpg?w=500&h=400&s=1",  # 替换为实际的接送服务图片URL
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
                                            # 预约日期
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "box",
                                                        "layout": "vertical",
                                                        "contents": [
                                                            {
                                                                "type": "text",
                                                                "text": "📅",
                                                                "size": "sm",
                                                                "align": "center"
                                                            }
                                                        ],
                                                        "width": "40px"
                                                    },
                                                    {
                                                        "type": "box",
                                                        "layout": "vertical",
                                                        "contents": [
                                                            {
                                                                "type": "text",
                                                                "text": "接駁日期",
                                                                "color": "#888888",
                                                                "size": "sm"
                                                            },
                                                            {
                                                                "type": "text",
                                                                "text": f"{date_with_weekday}",
                                                                "color": "#333333",
                                                                "weight": "bold",
                                                                "size": "md",
                                                                "margin": "sm"
                                                            }
                                                        ]
                                                    }
                                                ]
                                            },
                                            # 预约时间
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "box",
                                                        "layout": "vertical",
                                                        "contents": [
                                                            {
                                                                "type": "text",
                                                                "text": "⏰",
                                                                "size": "sm",
                                                                "align": "center"
                                                            }
                                                        ],
                                                        "width": "40px"
                                                    },
                                                    {
                                                        "type": "box",
                                                        "layout": "vertical",
                                                        "contents": [
                                                            {
                                                                "type": "text",
                                                                "text": "接駁時間",
                                                                "color": "#888888",
                                                                "size": "sm"
                                                            },
                                                            {
                                                                "type": "text",
                                                                "text": f"{time_range}",
                                                                "color": "#333333",
                                                                "weight": "bold",
                                                                "size": "md",
                                                                "margin": "sm"
                                                            }
                                                        ]
                                                    }
                                                ]
                                            },
                                            # 接驳地点
                                            {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "box",
                                                        "layout": "vertical",
                                                        "contents": [
                                                            {
                                                                "type": "text",
                                                                "text": "📍",
                                                                "size": "sm",
                                                                "align": "center"
                                                            }
                                                        ],
                                                        "width": "40px"
                                                    },
                                                    {
                                                        "type": "box",
                                                        "layout": "vertical",
                                                        "contents": [
                                                            {
                                                                "type": "text",
                                                                "text": "接駁地點",
                                                                "color": "#888888",
                                                                "size": "sm"
                                                            },
                                                            {
                                                                "type": "text",
                                                                "text": f"{location}",
                                                                "color": "#333333",
                                                                "weight": "bold",
                                                                "size": "md",
                                                                "margin": "sm",
                                                                "wrap": True
                                                            }
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
                                "body": {
                                    "backgroundColor": "#FFFFFF"
                                },
                                "footer": {
                                    "backgroundColor": "#F9F9F9",
                                    "separator": True
                                }
                            }
                        })
        # 发送消息
        line_bot_api.reply_message(event.reply_token, flex_message)

    elif any(keyword in event.message.text for keyword in ["服务", "预约", "小程序", "订票", "接驳","服務", "預約", "訂票", "接駁","APP","订单","訂單","app","我要预订","我要預訂"]):
        # 发送 Flex Message 作为默认回复
        reply_text = "為了方便您的旅行，請通過我們的小程序進行訂票"
        reply_userid = user_id
        liff_url = "https://liff.line.me/2006997627-KaPeq5n1"
        flex_message = FlexSendMessage(
            alt_text="【小程序】",
             contents={
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://mir-s3-cdn-cf.behance.net/projects/404/13647d144621821.Y3JvcCwyMDY3LDE2MTYsMCwxMDc.png",
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
                        "text": "金門通",
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
                        "text": "Powered by 金門通",
                        "size": "xxs",
                        "align": "center"
                    }
                ],
                "flex": 0
                }
            }
        )
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=reply_text), flex_message])
        print(reply_userid)
    else:
        reply_text = "抱歉，我沒有聽懂您的意思👀。請嘗試輸入“幫助”，“服務”，“預約”或“人工電話”以獲取幫助。"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text, quick_reply=quick_reply))
    

# @app.get("/bookings")
# def get_bookings():
#     return {"bookings": user_bookings}  # 返回最新的 JSON 数据

from datetime import datetime, timedelta
from linebot.models import FlexSendMessage

# 模拟全局变量（你实际应该从数据库或 json 文件加载）
user_bookings = {}

async def send_reminder():
    """定时检查所有预约，并提前 60 分钟发送提醒"""
    now = datetime.now()
    now_str = now.strftime("%H:%M")
    current_date = now.strftime("%Y-%m-%d")
    weekday_num = now.weekday()
    weekday_chinese = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}.get(weekday_num, "")

    for user_id, bookings in list(user_bookings.items()):
        if isinstance(bookings, list):
            for booking in bookings:
                await process_booking(user_id, booking, now, now_str, current_date, weekday_chinese)
        elif isinstance(bookings, dict):
            await process_booking(user_id, bookings, now, now_str, current_date, weekday_chinese)
        else:
            print(f"⚠️ 不支援的資料格式 for user {user_id}")


async def process_booking(user_id, booking_info, now, now_str, current_date, weekday_chinese):
    location = booking_info.get('location', '未知')
    booking_date = booking_info.get('date')
    booking_time_str = booking_info.get('time')

    # 解析日期
    if isinstance(booking_date, datetime):
        booking_date = booking_date.date()
    elif isinstance(booking_date, str):
        try:
            booking_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
        except Exception as e:
            print(f"⚠️ 日期格式錯誤: {booking_date}, Error: {e}")
            return

    if booking_date and booking_time_str:
        try:
            booking_time = datetime.strptime(booking_time_str, "%H:%M").time()
            reminder_time = (datetime.combine(datetime.today(), booking_time) - timedelta(minutes=60)).strftime("%H:%M")
            date_with_weekday = f"{booking_date}({weekday_chinese})"

            if current_date == booking_date.strftime("%Y-%m-%d") and now_str == reminder_time:
                print(f"📤 Sending reminder to: User {user_id} at {booking_date} {booking_time_str}, Location: {location}")
                
                end_time = (datetime.combine(datetime.today(), booking_time) + timedelta(minutes=60)).time()
                time_range = f"{booking_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"

                flex_message = FlexSendMessage(
                    alt_text="⏰ 接駁服務提醒",
                    contents={
                        "type": "bubble",
                        "header": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
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
                                        }
                                    ]
                                }
                            ]
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
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
                                        "uri": "https://liff.line.me/2006997627-KaPeq5n1"
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
                                    "text": "Powered by 金門通",
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
                )

                # 發送提醒訊息
                line_bot_api.push_message(user_id, flex_message)

        except ValueError as e:
            print(f"⚠️ 時間格式錯誤: {booking_time_str}, Error: {e}")
    else:
        print(f"⚠️ 預約資料不完整 for user {user_id}: {booking_info}")

async def schedule_checker():
    """定时任务：每 60 秒检查一次是否有需要提醒的用户"""
    while True:
        await send_reminder()
        await asyncio.sleep(60)

@app.on_event("startup")
async def startup_event():
    global user_bookings
    user_bookings = get_all_bookings()  # 从 JSON 文件加载数据
    asyncio.create_task(schedule_checker())  # 启动定时任务
    asyncio.create_task(check_json_periodically())  # 服务器启动时启动检查任务

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



# def save_user_bookings():
#     """保存用户预定数据到 JSON 文件"""
#     with open(USER_BOOKINGS_FILE, 'w', encoding='utf-8') as f:
#         for user_id, booking_info in user_bookings.items():
#             if isinstance(booking_info, list):
#                 for booking in booking_info:
#                     if 'location' not in booking:
#                         booking['location'] = '未知'
#                     if 'date' not in booking:
#                         booking['date'] = datetime.now().strftime("%Y-%m-%d")  # Set default date
#                     if 'time' not in booking:
#                         booking['time'] = ''  # Ensure 'time' field exists
#             else:
#                 if 'location' not in booking_info:
#                     booking_info['location'] = '未知'
#                 if 'date' not in booking_info:
#                     booking_info['date'] = datetime.now().strftime("%Y-%m-%d")  # Set default date
#                 if 'time' not in booking_info:
#                     booking_info['time'] = ''  # Ensure 'time' field exists
#         json.dump(user_bookings, f, ensure_ascii=False, indent=4)

# 存储用户 ID 和 预订时间，时间和地点
# USER_BOOKINGS_FILE = 'user_bookings.json'
# user_bookings = {}  


# def load_user_bookings():
#     global user_bookings
#     try:
#         with open('user_bookings.json', 'r', encoding='utf-8') as f:
#             user_bookings = json.load(f)
#             # print("🔄 JSON 数据已更新:", user_bookings)
#             # Ensure every booking has a "time" and "location"
#             for user_id, bookings in user_bookings.items():
#                 if isinstance(bookings, list):  # Handle list of bookings
#                     for booking_info in bookings:
#                         booking_info.setdefault('location', '未知')  # Set default location if missing
#                         booking_info.setdefault('time', '')  # Ensure 'time' field exists
#                 else:  # Handle single booking
#                     bookings.setdefault('location', '未知')
#                     bookings.setdefault('time', '')
                    
#             return user_bookings
#     except FileNotFoundError:
#         print("用户预定文件未找到，返回空的预定数据")
#         return {}
#     except json.JSONDecodeError:
#         print("JSON 数据格式错误")
#         return {}

# user_bookings = load_user_bookings()
# save_user_bookings()
