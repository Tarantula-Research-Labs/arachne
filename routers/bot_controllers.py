from fastapi import APIRouter, HTTPException
import subprocess
router = APIRouter()


@router.post("/bot/start", tags=["Bot Controllers"])
def start_bot():
    try:
        subprocess.run(["sudo", "systemctl", "start", "trading-bot"], check=True)
        return {"status": "bot started"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bot/stop", tags=["Bot Controllers"])
def stop_bot():
    try:
        subprocess.run(["sudo", "systemctl", "stop", "trading-bot"], check=True)
        return {"status": "bot stopped"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bot/restart", tags=["Bot Controllers"])
def restart_bot():
    try:
        subprocess.run(["sudo", "systemctl", "restart", "trading-bot"], check=True)
        return {"status": "bot restarted"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))