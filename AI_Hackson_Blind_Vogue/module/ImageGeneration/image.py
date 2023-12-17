from openai import OpenAI
from translate import Translator
import configparser
from pathlib import Path
import pandas as pd
config = configparser.ConfigParser()
relative_path = "../../config/config.ini"
file_path = (Path(__file__).parent / relative_path).resolve()
config.read(file_path)

api_key = config['API_KEYS']['IMG_VIOSION_KEY']


def translate_text(text, target_language='en', source_language='zh-TW'):
    translator= Translator(to_lang=target_language, from_lang=source_language)
    translation = translator.translate(text)
    return translation

def ImageGanerate(desc):
    client = OpenAI(api_key=api_key)
    desc = translate_text(desc)
    print(desc)
    response = client.images.generate(
    model="dall-e-3",
    prompt=desc,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    image_url = response.data[0].url

    desc_response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "假如我是衣服的王牌銷售，幫我針對衣服做出詳細介紹(例如:材質、顏色、場合、舒適度、圖案、花紋、版型、金額(可以自己預設)等)?，不要說與衣服介紹無關的話(例如這是一幅插畫等)，介紹必須生動吸引人和簡潔"},
            {
            "type": "image_url",
            "image_url": {
                "url": image_url,
            },
            },
        ],
        }
    ],
    max_tokens=250,
    )

    wear_desc = desc_response.choices[0].message.content

    print(f"img prompt : {desc}")
    print(f"image_url : {image_url}")
    print(f"wear_desc : {wear_desc}")

    return image_url, wear_desc



def ImageGenerate2(descriptions):
    client = OpenAI(api_key=api_key)
    generated_descriptions = []
    translated_desc = []
    for desc in descriptions:
        # 翻譯描述
        translated_desc.append(translate_text(desc)) 
        # print(translated_desc)

        # content_text = 
    desc_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"此衣服描述為{translated_desc},提供簡單的我三樣資訊 風格 合適的場合 衣服上的圖案描述 每個資訊都要簡約幾字描述 但衣服上的圖案描述要詳盡 以一行輸出 "
            }
        ],
        max_tokens=150,
    )
    # print(translate_text)
    wear_desc = desc_response.choices[0].message.content
    generated_descriptions.append(wear_desc)

    return wear_desc

man_description_text = []
woman_description_text = []

relative_man_csv_path = 'csv/output_man.csv'
man_csv_path = (Path(__file__).parent / relative_man_csv_path).resolve()

relative_woman_csv_path = 'csv/output_woman.csv'
woman_csv_path = (Path(__file__).parent / relative_woman_csv_path).resolve()

df = pd.read_csv(man_csv_path)

# ImageGanerate('西裝')
for index, row in df.iloc[:50].iterrows():
    

    elements = [row.iloc[0],row.iloc[2],row.iloc[3], row.iloc[4]]
    # print(elements)
    description = ImageGenerate2(elements)
    print(description)
    man_description_text.append(description)

man_description_text.extend([None] * (len(df) - len(man_description_text)))

df['description'] = man_description_text
df.to_csv('output_man.csv', index=False, encoding='utf-8')
# -------woman------------
df = pd.read_csv(woman_csv_path)

# ImageGanerate('西裝')
for index, row in df.iloc[:50].iterrows():
    

    elements = [row.iloc[0],row.iloc[2],row.iloc[3], row.iloc[4]]
    # print(elements)
    description = ImageGenerate2(elements)
    print(description)
    woman_description_text.append(description)

woman_description_text.extend([None] * (len(df) - len(woman_description_text)))

df['description'] = woman_description_text
df.to_csv('output_woman.csv', index=False, encoding='utf-8')