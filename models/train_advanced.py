import os
import sys
import torch
import torch.nn as nn
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql.database import SessionLocal
from sql.models import ProcessedFeatures

class SimpleLSTM(nn.Module):
    def __init__(self, input_size, hidden_size=16, num_layers=1):
        super(SimpleLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
        
    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

def train_advanced():
    print("Loading engineered features for deep learning...")
    db = SessionLocal()
    df = pd.read_sql(db.query(ProcessedFeatures).statement, db.bind)
    db.close()
    
    if df.empty:
        print("No processed features found.")
        return
        
    df = df.sort_values('date').set_index('date')
    df['target_wti_next_day'] = df['wti_usd_per_barrel'].shift(-1)
    df = df.dropna(subset=['target_wti_next_day'])
    
    features = ['wti_usd_per_barrel', 'wti_lag_1', 'wti_ma_7', 'event_intensity_score']
    
    # Scale variables using a simple proxy max/min
    cols_to_scale = features + ['target_wti_next_day']
    mins = df[cols_to_scale].min()
    maxs = df[cols_to_scale].max()
    
    df[cols_to_scale] = (df[cols_to_scale] - mins) / (maxs - mins + 1e-8)
        
    seq_len = 5
    X, y = [], []
    
    for i in range(len(df) - seq_len):
        X.append(df[features].iloc[i:i+seq_len].values)
        y.append(df['target_wti_next_day'].iloc[i+seq_len])
        
    X = torch.tensor(np.array(X), dtype=torch.float32)
    y = torch.tensor(np.array(y), dtype=torch.float32).view(-1, 1)
    
    model = SimpleLSTM(input_size=len(features))
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    
    print("Training PyTorch LSTM model...")
    epochs = 10
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
        
    print(f"Final epoch {epochs} simulated loss: {loss.item():.4f}")
    
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    model_path = os.path.join(os.path.dirname(__file__), 'lstm_model.pth')
    torch.save(model.state_dict(), model_path)
    print(f"PyTorch model saved to {model_path}")

if __name__ == "__main__":
    train_advanced()
