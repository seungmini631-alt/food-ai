import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import base64

app = FastAPI()

# CORS 설정 (플러터 앱 통신 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Render 환경변수(API_KEY)에서 OpenAI 키를 읽어옵니다.
api_key = os.getenv("API_KEY")
if not api_key:
    # 혹시 환경변수가 안 들어왔을 경우를 대비한 안전 장치
    print("WARNING: API_KEY environment variable is missing!")

client = OpenAI(api_key=api_key)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Food AI Server is running!"}

@app.post("/analyze-food")
async def analyze_food(file: UploadFile = File(...)):
    try:
        # 파일 읽기 및 base64 인코딩
        contents = await file.read()
        base64_image = base64.b64encode(contents).decode('utf-8')

        # Vision AI 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "이 음식 사진을 보고 음식이름, 대략적인 칼로리, 영양성분을 친절하게 한국어로 설명해줘."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )

        result_text = response.choices[0].message.content
        return {"result": result_text}

    except Exception as e:
        print(f"Error during analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))