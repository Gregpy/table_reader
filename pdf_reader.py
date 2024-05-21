
import PyPDF2
import json
import os
import time
import traceback
import pandas as pd
from dotenv import load_dotenv
import openai
# import pdfplumber


load_dotenv()

tread = r'ex_tables\foo.pdf'
pdfname = tread.split('\\')[-1].split('.')[0]
# print(pdfname)
# raise            
# pypdf2 showed better results, keeping column names together if in different rows
# all_text = ''
# with pdfplumber.open(tread) as pdf:

#     for page in pdf.pages:

#         text = page.extract_text()
#         all_text += text
# print(all_text)

# print('\n\npypdf2\n\n')
reader = PyPDF2.PdfReader(tread)
all_text2 = ''
for page in reader.pages:

    text = page.extract_text()
    all_text2 += text

print(all_text2)

# print('match?', all_text2 == all_text)

data = {"Pos": ['1','2','3'], "Player": ['Sachin Tendular', 'Kumar Sangakkara', 'Ricky Ponting'],
         "Team": ['India', 'Sri Lanka', 'Australia'], 'Span': ['1989 -2012','2000 -2015','1995 -2012'],
         "Innings": ['452', '380', '365'], "Runs": ['18426', '14234', '13704'],
         "Highest Score": ['200','169','164'], "Average": ['44.83','41.98','42.03'],
         "Striking Rate": ['86.23','78.86','80.39']}
# with open('data.json', 'w') as f:
#     json.dump(data, f)



# with open('data.json') as f:
#     d = json.load(f)
#     print(d)

# df = pd.read_json('data.json')
# print(df)

gpt_model = 'gpt-3.5-turbo'  # update as new ones come out


client = openai.OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Say this is a test",
#         }
#     ],
#     model=gpt_model,
# )
# print(dir(chat_completion.choices[0].message.content))
# print(chat_completion.choices[0].message.content)#['message']['content'])


tries = 2
for i in range(tries):
    print(f'try {i}')
    try:

        msgs = [{
                "role": "system", "content": """You are an assistant who only searches for tables in text 
                and then only retuns them in json format only."""},
                {"role": "user", "content": """Return a json for any table you find in this text. 
                 What are the cricket stats?
                 Pos Player  Team  Span  Innings  Runs  Highest 
Score  Average  Striking
Rate
1 Sachin Tendular  India  1989 -2012  452 18426  200 44.83  86.23
2 Kumar Sangakkara  Sri Lanka  2000 -2015  380 14234  169 41.98  78.86
3 Ricky Ponting  Australia  1995 -2012  365 13704  164 42.03  80.39"""},
                {"role": "assistant", "content": f"{data}"},
                {"role": "user", "content": """Return a json for any table you find in this text.
                 Q: What is sqrt(34328 * 2438)"""},
                {"role": "assistant", "content": ""},
                {"role": "user", "content": """Return a json for any table you find in this text.
                 Hello, how are you?"""},
                {"role": "assistant", "content": ""},
                {"role": "user", "content": f"""Return a json for any table you find in this text.
                 {all_text2}"""}
                 ]
        # time.sleep(0.1)
        print(f"Before call {time.perf_counter()}")
        response = client.chat.completions.create(
            model=gpt_model,
            messages=msgs,
            temperature=0,
        )
        print(f"After call {time.perf_counter()}")
        print('The table in json is -- ', response.choices[0].message.content)
        print('response tokens: ', response.usage.total_tokens)
        with open(f'{pdfname}.json', 'w') as f:
            json.dump(response.choices[0].message.content, f)
        # print(response)
        break

    except openai.RateLimitError as oe:
        print(traceback.format_exc())
        print('exception', oe)
        print('sleeping 10 s')
        time.sleep(10)
        continue
    except Exception as e:
        print(traceback.format_exc())
        print('exception', e)
        if i == tries - 1:
            print('failed result')
            raise ValueError
        continue

print(f"finish {time.perf_counter()}")
