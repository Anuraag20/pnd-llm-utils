import google.generativeai as genai
import os
import typing_extensions as tye
from typing import Optional
from datetime import datetime


'''
class Schedule(tye.TypedDict):
    datetime: Optional[str]
    exchange: Optional[str]
    pair: Optional[str] = USDT
    guess: Optional[bool]

'''

genai.configure(api_key = '')

model = genai.GenerativeModel("gemini-1.5-flash")

with open('prompt-test.txt') as f:
    
    prompt = ''.join(f.readlines())

message = '''

‼PUMP ANNOUNCEMENT‼

Exactly 24 hours remain until the start of the pump! The market has risen this week, and the price of Bitcoin is hovering around $60,000, so we expect a bigger pump than last Sunday.

MEXC Pump Details:
Date: September 15
Day: Sunday
Time: 6 PM (18:00)
Timezone: GMT+1 (London Time)
Exchange: MEXC.com
Pair: USDT

Our VIP members have just received the name of the coin we will pump tomorrow and are already starting to prepare to take their positions and secure profits from the pump.
We ask all free members to read our MEXC Pump Guide to prepare for the pump.

For any inquiries about pumps, exchanges, trading, VIP membership, or anything else, please contact our support team at: @Insider_Support_Team.

'''

result = model.generate_content(
    [prompt, message]
)
print(result.text)


