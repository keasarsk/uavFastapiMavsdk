from fastapi import FastAPI

from Location_log import Location_log

app = FastAPI()

log = Location_log()
lo = []
@app.get("/hello")
async def root():
    if await log.run():     
        return log.location
    else:
        return log.location
    # return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)
