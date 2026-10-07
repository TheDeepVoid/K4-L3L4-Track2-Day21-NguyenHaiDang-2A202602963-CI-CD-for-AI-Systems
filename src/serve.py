from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# Cloud SDK: azure-storage-blob (Azure) | google-cloud-storage (GCP) | boto3 (AWS)
from azure.storage.blob import BlobServiceClient
import joblib
import os

app = FastAPI()

# Doc ten container tu bien moi truong (duoc dat trong systemd service)
ARTIFACT_BUCKET = os.environ["ARTIFACT_BUCKET"]
MODEL_KEY = "artifacts/current/model.joblib"
MODEL_PATH = os.path.expanduser("~/models/model.joblib")

# Connection string cho Azure Blob (duoc dat trong systemd service)
AZURE_STORAGE_CONNECTION_STRING = os.environ["AZURE_STORAGE_CONNECTION_STRING"]


def download_model():
    """
    Tai file model.joblib tu cloud storage ve may khi server khoi dong.

    Ham nay duoc goi mot lan khi module duoc import. Xac thuc bang connection
    string cua Azure (duoc dat trong systemd service).
    """
    # TODO 1: Tao BlobServiceClient tu connection string
    client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

    # TODO 2: Lay container va blob tuong ung
    container = client.get_container_client(ARTIFACT_BUCKET)
    blob = container.get_blob_client(MODEL_KEY)

    # TODO 3: Tai file model xuong may
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        f.write(blob.download_blob().readall())

    # TODO 4: In thong bao thanh cong
    print("Model da duoc tai xuong tu cloud storage.")


download_model()
model = joblib.load(MODEL_PATH)


class ScoreRequest(BaseModel):
    features: list[float]


@app.get("/healthz")
def healthz():
    """
    Endpoint kiem tra suc khoe server.
    GitHub Actions goi endpoint nay sau khi deploy de xac nhan server dang chay.

    Tra ve: {"status": "ok"}
    """
    # TODO 5: Tra ve dict {"status": "ok"}
    return {"status": "ok"}


@app.post("/score")
def score(req: ScoreRequest):
    """
    Endpoint suy luan chinh.

    Dau vao : JSON {"features": [f1, f2, ..., f10]}
    Dau ra  : JSON {"prediction": <0|1>, "label": <"thu_nhap_thap"|"thu_nhap_cao">}

    Thu tu 10 dac trung (khop voi thu tu trong FEATURE_NAMES cua test):
        age, workclass, education_num, marital_status, occupation,
        relationship, sex, capital_gain, capital_loss, hours_per_week
    """
    # TODO 6: Kiem tra so luong dac trung.
    # Neu len(req.features) != 10, raise HTTPException(status_code=400, ...)
    if len(req.features) != 10:
        raise HTTPException(
            status_code=400, detail="Expected 10 features (adult income)"
        )

    # TODO 7: Goi model.predict([req.features]) de lay ket qua du doan.
    pred = model.predict([req.features])

    # TODO 8: Tra ve dict chua "prediction" (int) va "label" (string).
    # Nhan tuong ung: 0 -> "thu_nhap_thap", 1 -> "thu_nhap_cao"
    prediction = int(pred[0])
    label = "thu_nhap_cao" if prediction == 1 else "thu_nhap_thap"
    return {"prediction": prediction, "label": label}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
