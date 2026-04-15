## 
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return JSONResponse(
        status_code=200,
        content={"message": "API is running"}
    )

@app.get("/health")
def health():
    return JSONResponse(
        status_code=200,
        content={"message": "healthy"}
    )

@app.get("/me")
def me():
    return JSONResponse(
        status_code=200,
        content={
            "Name": "Oluwatobiloba Reuben Adeje",
            "Email": "oluwatobilobaadeje59@gmail.com",
            "GitHub": "https://github.com/Tobilee10/hng-internship-journey"
        }
    )