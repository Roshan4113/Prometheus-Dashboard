from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests, time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PROM_URL = "http://localhost:9090/api/v1/query_range"

# Serve dashboard HTML
@app.get("/")
async def root():
    return HTMLResponse(open("templates/dashboard.html").read())

# Fetch metrics from Prometheus
@app.get("/metric_data")
def get_metric_data(
    metric: str = Query(...),
    start: int | None = None,
    end: int | None = None,
    step: str = "5s"
):
    if not end:
        end = int(time.time())
    if not start:
        start = end - 300  # last 5 minutes

    resp = requests.get(PROM_URL, params={
        "query": metric,
        "start": start,
        "end": end,
        "step": step
    })
    data = resp.json()



    result = []
    for r in data.get("data", {}).get("result", []):
        result.append({"metric": r.get("metric", {}), "values": r.get("values", [])})

    return {"status": "success", "metric": metric, "result": result}



    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

