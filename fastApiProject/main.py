from fastapi import FastAPI, HTTPException
import requests
import uvicorn

app = FastAPI()


@app.get("/wetter/{stationids}")
def wetter_abfragen(stationids: str):
    url = f"https://dwd.api.proxy.bund.dev/v30/stationOverviewExtended?stationIds={stationids}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        return {"Wetter": data}
    else:
        raise HTTPException(status_code=response.status_code, detail="Fehler bei der Wetterabfrage")

@app.get("/pegelstand/{station}/{timeseries}")
def pegelstand_abfragen(station: str, timeseries: str):
    url = f"https://pegelonline.wsv.de/webservices/rest-api/v2/stations/{station}/{timeseries}/measurements.json"
    print(url)

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        return {"Pegelstand": data[-1]}
    else:
        raise HTTPException(status_code=response.status_code, detail="Fehler bei der Pegelstandabfrage")

if __name__ == "__main__":
    uvicorn.run(app)
