import time
import streamlit as st
import random
import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

gua_dict = {
    '阳阳阳': '乾',
    '阴阴阴': '坤',
    '阴阳阳': '兑',
    '阳阴阳': '震',
    '阳阳阴': '巽',
    '阴阳阴': '坎',
    '阳阴阴': '艮',
    '阴阴阳': '离'
}

number_dict = {
    0: '初爻',
    1: '二爻',
    2: '三爻',
    3: '四爻',
    4: '五爻',
    5: '六爻',
}

with open('gua.json') as gua_file:
  file_contents = gua_file.read()
des_dict = json.loads(file_contents)


st.set_page_config(
    page_title="AI Fortune Telling｜liu yao divining",
    page_icon="🔮",
    layout="centered",
)


st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)


st.markdown('## AI Fortune Telling｜LIU YAO Divining')
st.markdown(""" 

>This website is for entertainment purposes only and is not intended for fortune-telling, superstition, or divination. All results are randomly generated, and we strongly advise users not to make any decisions based on its content.

>Furthermore, the process of generating results is for reference purposes only and is just a part of the game's flow, not representing any orthodox practice.

>This website is purely for testing and entertainment and is not allowed for commercial use. All content should not be considered real, and minors should refrain from using it. We urge all users to approach it with a rational mindset and maintain an attitude of entertainment. Do not rely on or deeply believe in its results.
             
[AI Chat With God](https://aigod.sense-ocean.com)
🥺 "Thank you for using! Have fun, and remember to share with friends to enjoy!"
""")
st.markdown("""
            
            In the Six-Yao Divination, you will toss three coins six times. Based on the results of the coins (heads or tails), you will determine the yin and yang lines for each of the six throws. These six lines will then form two hexagrams, corresponding to one of the sixty-four hexagrams in the I Ching.

            The six yin and yang lines will represent six yao, and the combination of these six yao will form two hexagrams, which in turn correspond to specific hexagram descriptions. You can then interpret the hexagram descriptions for a random reading.

            To ensure usability and cost constraints, please note that you can only ask one question at a time. Please ask your question carefully.
            
            """)

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": [{"type": "text", "content": "Tell me your question in your heart ❤️"}]
    }]
if "disable_input" not in st.session_state:
    st.session_state.disable_input = False

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        for content in message["content"]:
            if content["type"] == "text":
                st.markdown(content["content"])
            elif content["type"] == "image":
                st.image(content["content"])
            elif content["type"] == "video":
                st.video(content["content"])


def add_message(role, content, delay=0.05):
     with st.chat_message(role):
        message_placeholder = st.empty()
        full_response = ""

        for chunk in list(content):
            full_response += chunk + ""
            time.sleep(delay)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)


def get_3_coin():
    return [random.randint(0, 1) for _ in range(3)]

def get_yin_yang_for_coin_res(coin_result):
    return "阳" if sum(coin_result) > 1.5 else "阴"

def get_number_for_coin_res(coin_result):
    return 1 if sum(coin_result) > 1.5 else 0

def format_coin_result(coin_result, i):
    return f"{number_dict[i]} 为 " + "".join([f"{'背' if i>0.5 else '字'}" for i in coin_result]) + " 为 " + get_yin_yang_for_coin_res(coin_result)

def disable():
    st.session_state["disable_input"] = True

if question := st.chat_input(placeholder="Enter your inner question.", key='input', disabled=st.session_state.disable_input, on_submit=disable):
    add_message("user", question)
    first_yin_yang = []
    for i in range(3):
        coin_res = get_3_coin()
        first_yin_yang.append(get_yin_yang_for_coin_res(coin_res))
        add_message("assistant", format_coin_result(coin_res, i))

    first_gua = gua_dict["".join(first_yin_yang)]
    add_message("assistant", f"您的首卦为：{first_gua}")

    second_yin_yang = []
    for i in range(3, 6):
        coin_res = get_3_coin()
        second_yin_yang.append(get_yin_yang_for_coin_res(coin_res))
        add_message("assistant", format_coin_result(coin_res, i))
    second_gua = gua_dict["".join(second_yin_yang)]
    add_message("assistant", f"您的次卦为：{second_gua}")

    gua = second_gua + first_gua
    gua_des = des_dict[gua]
    add_message("assistant", f"""
        六爻结果: {gua}  
        卦名为：{gua_des['name']}   
        {gua_des['des']}   
        卦辞为：{gua_des['sentence']}   
    """)

    with st.spinner('In the process of loading the interpretation, please wait a moment. ......'):

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [{"role":"system","content":"You are a divination expert from a prestigious Chinese Six Yao lineage. Your task is to provide valuable advice to those seeking divination based on their questions and the resulting hexagrams. Your responses should be grounded in an understanding of the hexagrams while also aiming to convey optimism and a positive attitude, guiding the diviners towards constructive paths of development."},
                        {"role":"user","content":f"""
                        The thing is：{question},
                        The result of the Six Yao divination is:：{gua},
                        The name of the hexagram is:：{gua_des['name']},
                        {gua_des['des']},
                        The hexagram's text is:：{gua_des['sentence']}"""},
                        ],
            temperature=0.7,
            max_tokens=500,
            top_p=0.95,
            frequency_penalty=0.5,
            presence_penalty=0.1,
            stop=None)
    add_message("assistant", response.choices[0].message.content)
    time.sleep(0.1)

    add_message("assistant", """[AI Chat With God](https://aigod.sense-ocean.com)  
                    Thank you for using! Have fun, and remember to share with friends to enjoy!""", 0.01)