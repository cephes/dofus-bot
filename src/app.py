from fastapi import FastAPI, HTTPException
import subprocess
import json
import os

app = FastAPI(title="Dofus Bot Orchestrator")

CORE_BINARY = os.path.join(os.path.dirname(__file__), "../../core/target/debug/dofus-core")

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/bots/start")
async def start_bot():
    try:
        # Stub: call Rust core with dummy pcap
        result = subprocess.run([CORE_BINARY, "--pcap", "dummy.pcap"], capture_output=True, text=True)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {"message": "Bot started", "data": data}
        else:
            raise HTTPException(status_code=500, detail="Failed to start bot")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bots/stop")
async def stop_bot():
    try:
        # Stub: call Rust core
        result = subprocess.run([CORE_BINARY], capture_output=True, text=True)
        if result.returncode == 0:
            data = json.loads(result.stdout) if result.stdout else {}
            return {"message": "Bot stopped", "data": data}
        else:
            raise HTTPException(status_code=500, detail="Failed to stop bot")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bots/status")
async def bot_status():
    try:
        # Stub: call Rust core
        result = subprocess.run([CORE_BINARY], capture_output=True, text=True)
        if result.returncode == 0:
            data = json.loads(result.stdout) if result.stdout else {}
            return {"status": "running", "data": data}
        else:
            return {"status": "stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))