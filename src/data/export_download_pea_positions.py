import os
import shutil

downloads = os.path.expanduser("~\Downloads")
target =  os.path.expanduser("~\PROJET-QUANT\pea-trading-bot\data")
prefix = "export-positions-instantanees" 
latest_file = max(
    [f for f in os.listdir(downloads) if prefix in f and f.endswith(".csv")],
    key=lambda f: os.path.getctime(os.path.join(downloads, f))
)
shutil.move(os.path.join(downloads, latest_file), os.path.join(target, "positions.csv"))
