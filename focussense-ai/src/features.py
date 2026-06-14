import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
 
print("Feature engine started...")
 
def calculate_features(df):
    """Extract intelligent features from activity data"""
    
    if df.empty:
        return pd.DataFrame()
    
    # Convert time
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df = df.dropna(subset=['time'])
    df = df.sort_values('time').reset_index(drop=True)
    
    # 30-second buckets
    df['bucket'] = df['time'].dt.floor('30s')
    
    # Count different event types
    features = df.groupby('bucket').agg({
        'event': 'count'
    }).rename(columns={'event': 'total_actions'})
    
    # Mouse movements
    mouse_moves = df[df['event'] == 'mouse_move'].groupby('bucket').size()
    features['mouse_moves'] = mouse_moves
    
    # Mouse clicks (left + right)
    mouse_clicks = df[df['event'].isin(['mouse_left', 'mouse_right'])].groupby('bucket').size()
    features['mouse_clicks'] = mouse_clicks
    
    # Keyboard presses
    keyboard_presses = df[df['event'] == 'key_press'].groupby('bucket').size()
    features['keyboard_presses'] = keyboard_presses
    
    # Fill NaN with 0
    features = features.fillna(0)
    
    # Feature 1: Idle Detection (gaps between actions)
    # If there's a gap > 10 seconds in a bucket, likely idle
    features['max_gap'] = 0.0
    for bucket in features.index:
        bucket_df = df[df['bucket'] == bucket].sort_values('time')
        if len(bucket_df) > 1:
            time_diffs = bucket_df['time'].diff().dt.total_seconds()
            features.loc[bucket, 'max_gap'] = time_diffs.max()
    
    # Feature 2: Action Intensity (actions per second in the bucket)
    features['action_intensity'] = features['total_actions'] / 30.0  # 30-second bucket
    
    # Feature 3: Input Type Ratio
    features['keyboard_ratio'] = features['keyboard_presses'] / (features['total_actions'] + 0.1)
    features['mouse_ratio'] = (features['mouse_moves'] + features['mouse_clicks']) / (features['total_actions'] + 0.1)
    features['click_ratio'] = features['mouse_clicks'] / (features['total_actions'] + 0.1)
    
    # Feature 4: Typing vs Moving (coding/writing vs browsing)
    # High keyboard + low mouse = focused work
    # High mouse + low keyboard = browsing
    features['typing_focus'] = features['keyboard_presses'] / (features['mouse_moves'] + 1)
    
    # Feature 5: Activity Consistency
    # Are actions spread evenly or clustered?
    # (This would need timestamp data, simplified here)
    features['is_clustered'] = (features['action_intensity'] > 0.2).astype(int)
    
    # Idle Label (the ground truth)
    # Someone is IDLE if:
    # 1. Very few actions (< 2 actions in 30 sec), OR
    # 2. Very long gaps between actions (> 15 sec), OR
    # 3. Only mouse movement with no interaction (mouse_ratio > 0.95 and actions < 3)
    
    features['is_idle'] = (
        (features['total_actions'] < 2) |
        (features['max_gap'] > 15) |
        ((features['mouse_ratio'] > 0.95) & (features['total_actions'] < 3))
    ).astype(int)
    
    # Reset index to make bucket a column
    features = features.reset_index()
    
    # Clean up infinite/NaN values
    features = features.replace([np.inf, -np.inf], 0).fillna(0)
    
    return features
 
while True:
    try:
        # Load activity log
        df = pd.read_csv("data/activity_log.csv")
        
        # Calculate features
        features = calculate_features(df)
        
        if not features.empty:
            # Save features
            features.to_csv("data/features.csv", index=False)
            
            # Print summary
            idle_pct = (features['is_idle'].sum() / len(features) * 100) if len(features) > 0 else 0
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Processed {len(features)} buckets | Idle: {idle_pct:.1f}% | Last action intensity: {features['action_intensity'].iloc[-1]:.2f}")
        
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
    
    time.sleep(10)