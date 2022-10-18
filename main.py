from fastapi import FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse, JSONResponse


app = FastAPI()


@app.get('/')
@app.get('/index')
async def root():
    return 'Hello world'


def calculation(phrase: str):
    phrase = phrase.replace(' ', '+')
    print(phrase)
    try:
        result = eval(phrase)
    except(ValueError, SyntaxError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f' Error. Incorrect phrase {phrase}'
        )
    return(phrase, result)


@app.get('/eval')
async def get_calculation(phrase: str):
    try:
        phrase, result = calculation(phrase)
    except(HTTPException):
        return PlainTextResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f' Error. Incorrect phrase {phrase}'
        )
    return (f'{phrase}={result}')


@app.post('/eval')
async def post_calculation(phrase: str):
    phrase, result = calculation(phrase)

    return JSONResponse(
        content={
            'phrase': phrase,
            'result': result
        },
        status_code=status.HTTP_201_CREATED
    )
