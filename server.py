import base64
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware  # 👈 1. CORS 모듈 추가
from openai import OpenAI

app = FastAPI()

# 👈 2. 브라우저 차단 해제(CORS) 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 곳에서의 접속 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 요청 방식(POST, GET 등) 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 3. OpenAI API 키 설정
API_KEY = "dummy"
client = OpenAI(api_key=API_KEY)


@app.post("/analyze-food")
async def analyze_food(file: UploadFile = File(...)):
    image_bytes = await file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "사진 속 음식이 무엇인지 알려주고, 예상 칼로리와 간단한 특징을 한국어로 알려줘.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    return {"result": response.choices[0].message.content}
    