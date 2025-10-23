
# from fastapi import FastAPI, File, UploadFile, Form
# from fastapi.responses import JSONResponse
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import stats
# from sklearn.cluster import KMeans
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from io import BytesIO
# import warnings
# warnings.filterwarnings('ignore')

# app = FastAPI()

# # Define physiological ranges for scaling
# STANCE_RANGE = (600, 750)  # ms
# SWING_RANGE = (450, 550)   # ms  
# STRIDE_RANGE = (1150, 1250) # ms

# def generate_synthetic_database():
#     """
#     Generate 500 synthetic subjects with demographics and gait parameters
#     80% normal, 20% abnormal
#     """
#     np.random.seed(42)  # For reproducibility
    
#     n_subjects = 500
#     n_normal = 400  # 80%
#     n_abnormal = 100  # 20%
    
#     subjects = []
    
#     # Generate Normal Subjects (400)
#     for i in range(n_normal):
#         # Demographics
#         age = np.random.randint(18, 80)
#         gender = np.random.choice(['Male', 'Female'])
        
#         if gender == 'Male':
#             height = np.random.normal(175, 8)  # Male average height
#             weight = np.random.normal(75, 12)  # Male average weight
#         else:
#             height = np.random.normal(162, 7)  # Female average height
#             weight = np.random.normal(62, 10)  # Female average weight
        
#         # Age-adjusted normal gait parameters
#         age_factor = 1.0 if age < 65 else 1.1 + (age - 65) * 0.01  # Slower with age
        
#         # Normal gait parameters with some variation
#         stance_time = np.random.normal(675, 25) * age_factor
#         swing_time = np.random.normal(500, 20) * age_factor
#         stride_time = stance_time + swing_time
#         speed = np.random.normal(1.2, 0.15) / age_factor  # Slower with age
#         cadence = np.random.normal(110, 10) / age_factor
#         step_length = speed / (cadence / 60)
        
#         subjects.append({
#             'ID': f'N{i+1:03d}',
#             'Age': int(age),
#             'Gender': gender,
#             'Height': round(height, 1),
#             'Weight': round(weight, 1),
#             'StanceTime': round(stance_time, 2),
#             'SwingTime': round(swing_time, 2),
#             'StrideTime': round(stride_time, 2),
#             'Speed': round(speed, 2),
#             'Cadence': round(cadence, 1),
#             'StepLength': round(step_length, 2),
#             'Label': 'Normal'
#         })
    
#     # Generate Abnormal Subjects (100)
#     abnormal_patterns = ['slow_gait', 'long_stance', 'short_swing', 'variable_pattern', 'fast_compensatory']
    
#     for i in range(n_abnormal):
#         # Demographics
#         age = np.random.randint(18, 80)
#         gender = np.random.choice(['Male', 'Female'])
        
#         if gender == 'Male':
#             height = np.random.normal(175, 8)
#             weight = np.random.normal(75, 12)
#         else:
#             height = np.random.normal(162, 7)
#             weight = np.random.normal(62, 10)
        
#         # Choose abnormal pattern
#         pattern = np.random.choice(abnormal_patterns)
        
#         if pattern == 'slow_gait':  # Like Subject 4 from your data
#             stance_time = np.random.normal(780, 30)  # Long stance
#             swing_time = np.random.normal(300, 50)   # Short swing
#             speed = np.random.normal(0.7, 0.1)      # Slow speed
#             cadence = np.random.normal(85, 8)       # Low cadence
#         elif pattern == 'long_stance':
#             stance_time = np.random.normal(800, 25)
#             swing_time = np.random.normal(480, 30)
#             speed = np.random.normal(0.9, 0.15)
#             cadence = np.random.normal(95, 10)
#         elif pattern == 'short_swing':
#             stance_time = np.random.normal(720, 20)
#             swing_time = np.random.normal(350, 40)
#             speed = np.random.normal(0.85, 0.12)
#             cadence = np.random.normal(90, 8)
#         elif pattern == 'variable_pattern':
#             stance_time = np.random.normal(700, 50)  # High variability
#             swing_time = np.random.normal(450, 60)
#             speed = np.random.normal(1.0, 0.25)
#             cadence = np.random.normal(100, 20)
#         else:  # fast_compensatory
#             stance_time = np.random.normal(580, 15)  # Short stance
#             swing_time = np.random.normal(420, 25)   # Short swing
#             speed = np.random.normal(1.4, 0.2)      # Fast speed
#             cadence = np.random.normal(130, 15)     # High cadence
        
#         stride_time = stance_time + swing_time
#         step_length = speed / (cadence / 60)
        
#         subjects.append({
#             'ID': f'A{i+1:03d}',
#             'Age': int(age),
#             'Gender': gender,
#             'Height': round(height, 1),
#             'Weight': round(weight, 1),
#             'StanceTime': round(stance_time, 2),
#             'SwingTime': round(swing_time, 2),
#             'StrideTime': round(stride_time, 2),
#             'Speed': round(speed, 2),
#             'Cadence': round(cadence, 1),
#             'StepLength': round(step_length, 2),
#             'Label': 'Abnormal'
#         })
    
#     return pd.DataFrame(subjects)

# def train_health_classifier(df_synthetic):
#     """
#     Train a classifier to distinguish normal vs abnormal gait patterns
#     """
#     # Features for classification
#     feature_cols = ['Age', 'Height', 'Weight', 'StanceTime', 'SwingTime', 
#                    'StrideTime', 'Speed', 'Cadence', 'StepLength']
    
#     X = df_synthetic[feature_cols]
#     y = df_synthetic['Label']
    
#     # Encode gender if needed (not used in this version)
#     # Handle any missing values
#     X = X.fillna(X.mean())
    
#     # Split and train
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
#     # Scale features
#     scaler = StandardScaler()
#     X_train_scaled = scaler.fit_transform(X_train)
#     X_test_scaled = scaler.transform(X_test)
    
#     # Train classifier
#     clf = RandomForestClassifier(n_estimators=100, random_state=42)
#     clf.fit(X_train_scaled, y_train)
    
#     # Calculate accuracy
#     train_accuracy = clf.score(X_train_scaled, y_train)
#     test_accuracy = clf.score(X_test_scaled, y_test)
    
#     print(f"Health Classifier Training Accuracy: {train_accuracy:.3f}")
#     print(f"Health Classifier Test Accuracy: {test_accuracy:.3f}")
    
#     return clf, scaler

# def adaptive_threshold(pressure_data, contact_bias=0.7):
#     """Calculate adaptive thresholds using clustering approach"""
#     clean_data = pressure_data[pressure_data > 0.1].values.reshape(-1, 1)
    
#     if len(clean_data) < 10:
#         return 1.0, 1.0
    
#     kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
#     clusters = kmeans.fit_predict(clean_data)
    
#     cluster_0_mean = clean_data[clusters == 0].mean()
#     cluster_1_mean = clean_data[clusters == 1].mean()
    
#     if cluster_0_mean > cluster_1_mean:
#         contact_cluster_mean = cluster_0_mean
#         air_cluster_mean = cluster_1_mean
#     else:
#         contact_cluster_mean = cluster_1_mean  
#         air_cluster_mean = cluster_0_mean
    
#     landing_threshold = air_cluster_mean + contact_bias * (contact_cluster_mean - air_cluster_mean)
#     release_threshold = air_cluster_mean + (1 - contact_bias) * (contact_cluster_mean - air_cluster_mean)
    
#     return float(landing_threshold), float(release_threshold)

# def detect_gait_events(df, heel_col, m1_col):
#     """Detect heel strikes and toe-offs for one foot"""
#     heel_landing_thresh, heel_release_thresh = adaptive_threshold(df[heel_col])
#     m1_landing_thresh, m1_release_thresh = adaptive_threshold(df[m1_col])
    
#     # Heel strike detection
#     heel_landing_times = []
#     in_contact_heel = False
    
#     for i in range(len(df)):
#         pressure = df[heel_col].iloc[i]
#         if not in_contact_heel and pressure > heel_landing_thresh:
#             heel_landing_times.append(df['Time(ms)'].iloc[i])
#             in_contact_heel = True
#         elif in_contact_heel and pressure < heel_release_thresh:
#             in_contact_heel = False
    
#     # Toe-off detection
#     m1_release_times = []
#     in_contact_m1 = False
    
#     for i in range(len(df)):
#         pressure = df[m1_col].iloc[i]
#         if not in_contact_m1 and pressure > m1_landing_thresh:
#             in_contact_m1 = True
#         elif in_contact_m1 and pressure < m1_release_thresh:
#             m1_release_times.append(df['Time(ms)'].iloc[i])
#             in_contact_m1 = False
    
#     return heel_landing_times, m1_release_times

# def calculate_gait_parameters(heel_landing_times, m1_release_times):
#     """Calculate stance, swing, and stride times with cycle synchronization"""
#     if len(heel_landing_times) == 0 or len(m1_release_times) == 0:
#         return [], [], []
    
#     cycles = min(len(heel_landing_times), len(m1_release_times))
#     stance_times = []
#     swing_times = []
    
#     if m1_release_times[0] > heel_landing_times[0]:
#         for i in range(cycles):
#             if i < len(m1_release_times) and i < len(heel_landing_times):
#                 stance_time = m1_release_times[i] - heel_landing_times[i]
#                 if 300 < stance_time < 1000:
#                     stance_times.append(stance_time)
        
#         for i in range(len(stance_times) - 1):
#             if i + 1 < len(heel_landing_times) and i < len(m1_release_times):
#                 swing_time = heel_landing_times[i + 1] - m1_release_times[i]
#                 if 200 < swing_time < 800:
#                     swing_times.append(swing_time)
#     else:
#         for i in range(cycles - 1):
#             if i + 1 < len(heel_landing_times) and i + 1 < len(m1_release_times):
#                 stance_time = m1_release_times[i + 1] - heel_landing_times[i]
#                 if 300 < stance_time < 1000:
#                     stance_times.append(stance_time)
        
#         for i in range(len(stance_times)):
#             if i < len(heel_landing_times) and i < len(m1_release_times):
#                 swing_time = heel_landing_times[i] - m1_release_times[i]
#                 if 200 < swing_time < 800:
#                     swing_times.append(swing_time)
    
#     min_len = min(len(stance_times), len(swing_times))
#     stride_times = []
#     for i in range(min_len):
#         stride_times.append(stance_times[i] + swing_times[i])
    
#     return stance_times[:min_len], swing_times[:min_len], stride_times

# def scale_to_physiological_range(values, target_range):
#     """Scale values to fit within physiological range"""
#     if not values or len(values) == 0:
#         return []
    
#     current_mean = np.mean(values)
#     target_mean = np.mean(target_range)
#     scale_factor = target_mean / current_mean
    
#     scaled_values = [v * scale_factor for v in values]
#     min_target, max_target = target_range
#     scaled_values = [max(min_target, min(max_target, v)) for v in scaled_values]
    
#     return scaled_values

# def calculate_spatial_temporal_params(stride_times, total_time, distance_walked=5):
#     """Calculate speed, cadence, and step length"""
#     if not stride_times or len(stride_times) == 0:
#         return 0, 0, 0
    
#     avg_stride_time = np.mean(stride_times)
#     speed = distance_walked / (total_time / 1000)
#     cadence = (60 / (avg_stride_time / 1000)) * 2
#     step_length = speed / (cadence / 60)
    
#     return speed, cadence, step_length

# def analyze_asymmetry(left_params, right_params):
#     """Calculate asymmetry ratios and determine if gait is symmetric"""
#     ratios = []
#     param_names = ['Stance', 'Swing', 'Stride', 'Cadence']
#     relevant_params = 4
    
#     for i in range(relevant_params):
#         left, right = left_params[i], right_params[i]
#         if right != 0:
#             ratio = left / right
#             ratios.append(ratio)
#             print(f"{param_names[i]} Ratio (L/R): {ratio:.3f}")
    
#     if ratios:
#         avg_deviation = np.mean([abs(r - 1.0) for r in ratios])
#         print(f"Average Asymmetry Deviation: {avg_deviation:.3f}")
        
#         # Tight threshold: 5% deviation
#         if avg_deviation < 0.05:
#             return "SYMMETRIC", avg_deviation
#         else:
#             return "ASYMMETRIC", avg_deviation
    
#     return "INSUFFICIENT_DATA", 0

# def classify_health_status(subject_params, classifier, scaler, subject_demographics):
#     """Classify if subject shows normal or abnormal gait pattern"""
#     # Prepare feature vector
#     features = [
#         subject_demographics.get('age', 25),
#         subject_demographics.get('height', 170),
#         subject_demographics.get('weight', 70),
#         subject_params[0],  # stance
#         subject_params[1],  # swing  
#         subject_params[2],  # stride
#         subject_params[3],  # speed
#         subject_params[4],  # cadence
#         subject_params[5]   # step_length
#     ]
    
#     # Scale features
#     features_scaled = scaler.transform([features])
    
#     # Get prediction and probability
#     prediction = classifier.predict(features_scaled)[0]
#     probability = classifier.predict_proba(features_scaled)[0]
    
#     return prediction, max(probability)

# def comprehensive_gait_analysis(df1, subject_demographics=None):
#     """
#     Complete gait analysis pipeline with health classification
#     """
#     if subject_demographics is None:
#         subject_demographics = {'age': 25, 'height': 170, 'weight': 70}
    
#     print("=== COMPREHENSIVE GAIT ANALYSIS SYSTEM ===\n")
    
#     # Generate synthetic database and train classifier

#     synthetic_db = generate_synthetic_database()
    
#     print("Training health classifier...")
#     health_classifier, feature_scaler = train_health_classifier(synthetic_db)
#     print()
    
#     # Calculate total recording time
#     total_time = df1['Time(ms)'].iloc[-1] - df1['Time(ms)'].iloc[0]
#     print(f"Total Recording Time: {total_time:.0f} ms\n")
    
#     # Analyze Right Foot
#     print("--- RIGHT FOOT ANALYSIS ---")
#     heel_landing_right, m1_release_right = detect_gait_events(df1, 'Heel_R(kPa)', 'M1_R(kPa)')
#     stance_right, swing_right, stride_right = calculate_gait_parameters(heel_landing_right, m1_release_right)
    
#     if stance_right and swing_right and stride_right:
#         stance_right_scaled = scale_to_physiological_range(stance_right, STANCE_RANGE)
#         swing_right_scaled = scale_to_physiological_range(swing_right, SWING_RANGE)
#         stride_right_scaled = scale_to_physiological_range(stride_right, STRIDE_RANGE)
        
#         speed_right, cadence_right, step_length_right = calculate_spatial_temporal_params(
#             stride_right_scaled, total_time)
        
#         print(f"Average Stance Time: {np.mean(stance_right_scaled):.1f} ms")
#         print(f"Average Swing Time: {np.mean(swing_right_scaled):.1f} ms") 
#         print(f"Average Stride Time: {np.mean(stride_right_scaled):.1f} ms")
#         print(f"Speed: {speed_right:.2f} m/s")
#         print(f"Cadence: {cadence_right:.1f} steps/min")
#         print(f"Step Length: {step_length_right:.2f} m")
        
#         right_params = [np.mean(stance_right_scaled), np.mean(swing_right_scaled), 
#                        np.mean(stride_right_scaled), speed_right, cadence_right, step_length_right]
#     else:
#         print("Insufficient data for right foot analysis")
#         right_params = [0, 0, 0, 0, 0, 0]
    
#     print("\n--- LEFT FOOT ANALYSIS ---")
#     heel_landing_left, m1_release_left = detect_gait_events(df1, 'Heel_L(kPa)', 'M1_L(kPa)')
#     stance_left, swing_left, stride_left = calculate_gait_parameters(heel_landing_left, m1_release_left)
    
#     if stance_left and swing_left and stride_left:
#         stance_left_scaled = scale_to_physiological_range(stance_left, STANCE_RANGE)
#         swing_left_scaled = scale_to_physiological_range(swing_left, SWING_RANGE)
#         stride_left_scaled = scale_to_physiological_range(stride_left, STRIDE_RANGE)
        
#         speed_left, cadence_left, step_length_left = calculate_spatial_temporal_params(
#             stride_left_scaled, total_time)
        
#         print(f"Average Stance Time: {np.mean(stance_left_scaled):.1f} ms")
#         print(f"Average Swing Time: {np.mean(swing_left_scaled):.1f} ms")
#         print(f"Average Stride Time: {np.mean(stride_left_scaled):.1f} ms")
#         print(f"Speed: {speed_left:.2f} m/s")
#         print(f"Cadence: {cadence_left:.1f} steps/min")
#         print(f"Step Length: {step_length_left:.2f} m")
        
#         left_params = [np.mean(stance_left_scaled), np.mean(swing_left_scaled),
#                       np.mean(stride_left_scaled), speed_left, cadence_left, step_length_left]
#     else:
#         print("Insufficient data for left foot analysis")
#         left_params = [0, 0, 0, 0, 0, 0]
    
#     # Asymmetry Analysis
#     print("\n--- ASYMMETRY ANALYSIS ---")
#     symmetry_result, avg_deviation = analyze_asymmetry(left_params, right_params)
    
#     # Health Classification (using average of both feet)
#     print("\n--- HEALTH CLASSIFICATION ---")
#     if sum(right_params) > 0 and sum(left_params) > 0:
#         # Average bilateral parameters for health classification
#         avg_params = [(l + r) / 2 for l, r in zip(left_params, right_params)]
#         health_prediction, confidence = classify_health_status(
#             avg_params, health_classifier, feature_scaler, subject_demographics)
        
#         print(f"Gait Health Status: {health_prediction}")
#         print(f"Classification Confidence: {confidence:.3f}")
#     else:
#         health_prediction = "INSUFFICIENT_DATA"
#         confidence = 0.0
    
#     # Final Assessment
#     print(f"\n=== FINAL ASSESSMENT ===")
#     print(f"Bilateral Symmetry: {symmetry_result}")
#     if symmetry_result != "INSUFFICIENT_DATA":
#         print(f"Asymmetry Level: {avg_deviation*100:.1f}%")
    
#     print(f"Overall Gait Health: {health_prediction}")
#     if confidence > 0:
#         print(f"Health Confidence: {confidence*100:.1f}%")
    
#     # Clinical Interpretation
#     print(f"\n--- CLINICAL INTERPRETATION ---")
#     if symmetry_result == "SYMMETRIC" and health_prediction == "Normal":
#         print("✅ HEALTHY GAIT PATTERN")
#         print("   - Bilateral symmetry maintained")
#         print("   - Parameters within normal ranges")
#         print("   - No immediate concerns identified")
#     elif symmetry_result == "ASYMMETRIC" and health_prediction == "Normal":
#         print("⚠️  MINOR ASYMMETRY DETECTED")
#         print("   - Overall gait health appears normal")
#         print("   - Monitor asymmetry trends")
#         print("   - Consider bilateral strengthening")
#     elif symmetry_result == "SYMMETRIC" and health_prediction == "Abnormal":
#         print("⚠️  GAIT ABNORMALITY DETECTED")
#         print("   - Bilateral symmetry maintained")
#         print("   - Parameters deviate from healthy patterns")
#         print("   - Recommend clinical evaluation")
#     else:
#         print("🚨 MULTIPLE CONCERNS IDENTIFIED")
#         print("   - Both asymmetry and abnormal patterns detected")
#         print("   - Comprehensive clinical assessment recommended")
#         print("   - Consider referral to gait specialist")
    
#     return {
#         'symmetry': symmetry_result,
#         'asymmetry_deviation': avg_deviation,
#         'health_status': health_prediction,
#         'health_confidence': confidence,
#         'right_params': right_params,
#         'left_params': left_params
#     }

# # #Load and prepare data (you'll need to update column names based on your actual data)
# # df1 = pd.read_csv('New Datasets/pranjay1.csv')
# # column_names = ['CurrentTimeStamps','Time(ms)', 'M1_R(kPa)', 'M2_R(kPa)', 'Mid_R(kPa)', 'Heel_R(kPa)',
# #                 'M1_L(kPa)', 'M2_L(kPa)', 'Mid_L(kPa)', 'Heel_L(kPa)']
# # df1.columns = column_names

# # #Example usage:
# # subject_info = {'age': 21, 'height': 169, 'weight': 95}
# # results = comprehensive_gait_analysis(df1, subject_info)








# # ========== WRAPPER API ==========

# @app.post("/analyze-gait/")
# async def analyze_gait(
#     file: UploadFile = File(...),
#     age: int = Form(...),
#     height: float = Form(...),
#     weight: float = Form(...)
# ):
#     try:
#         contents = await file.read()
#         df1 = pd.read_csv(BytesIO(contents))

#         # Assign column names (as per your existing code)
#         column_names = ['CurrentTimeStamps','Time(ms)', 'M1_R(kPa)', 'M2_R(kPa)', 'Mid_R(kPa)', 'Heel_R(kPa)',
#                         'M1_L(kPa)', 'M2_L(kPa)', 'Mid_L(kPa)', 'Heel_L(kPa)']
#         df1.columns = column_names

#         subject_info = {'age': age, 'height': height, 'weight': weight}
#         results = comprehensive_gait_analysis(df1, subject_info)

#         return JSONResponse(content=results)

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})







#############################################################
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from io import BytesIO
import json
import numpy as np
import pandas as pd
import warnings

# Suppress warnings for a cleaner API log
warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------
# START: EXACT CODE BLOCK COPIED FROM USER'S combined.py SCRIPT
# 
# NOTE: Plotting functions and main/argparse blocks are omitted 
# as they are not needed for the FastAPI response logic.
# ---------------------------------------------------------------------

# Column alias mapping
COLUMN_ALIASES = {
    'time': ['Time(ms)', 'Time Difference in Milliseconds', 'CurrentTimeStamps', 'time', 'Timestamp'],
    'M1_R': ['M1_R(kPa)', 'IncipMat M1', 'Right_M1', 'M1_R', 'Right M1'],
    'M2_R': ['M2_R(kPa)', 'IncipMat M2', 'Right_M2', 'M2_R', 'Right M2'],
    'Mid_R': ['Mid_R(kPa)', 'IncipMat Middle', 'Right_Mid', 'Mid_R', 'Right Middle'],
    'Heel_R': ['Heel_R(kPa)', 'IncipMat Heel', 'Right_Heel', 'Heel_R', 'Right Heel'],
    'M1_L': ['M1_L(kPa)', 'Left1 M1', 'Left_M1', 'M1_L', 'Left M1'],
    'M2_L': ['M2_L(kPa)', 'Left1 M2', 'Left_M2', 'M2_L', 'Left M2'],
    'Mid_L': ['Mid_L(kPa)', 'Left1 Middle', 'Left_Mid', 'Mid_L', 'Left Middle'],
    'Heel_L': ['Heel_L(kPa)', 'Left1 Heel', 'Left_Heel', 'Heel_L', 'Left Heel'],
}

def find_column(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

def keep_dynamic(df, sensor_cols, threshold=1e-3, min_rows=10):
    """Keep rows where any sensor changes by > threshold (absolute diff)."""
    mask = np.zeros(len(df), dtype=bool)
    for col in sensor_cols:
        if col not in df.columns:
            continue
        # Ensure column is numeric before diff (added safeguard for API context)
        s = pd.to_numeric(df[col], errors='coerce').fillna(0)
        diff = s.diff().abs().fillna(0)
        mask = mask | (diff > threshold)
    filtered = df.loc[mask].reset_index(drop=True)
    if filtered.shape[0] < min_rows:
        # If too aggressive, return original with warning (print removed for API)
        return df.copy(), False
    return filtered.copy(), True

def compute_per_sensor_peak_stats(df, sensor_cols, rolling_window=30, flat_std_thresh=0.02, peak_height_mult=0.7):
    """
    Compute comprehensive per-sensor statistics (Code 1/2 parameters).
    Returns: peak_stats dict (per_sensor_peak_indices removed as it's for plotting)
    """
    peak_stats = {}
    from scipy.signal import find_peaks # Imported locally as it's needed here
    
    for col in sensor_cols:
        if col not in df.columns:
            continue
        s = df[col].copy().astype(float)
        rolling_std = s.rolling(window=rolling_window, center=True).std().fillna(0)
        flat_frac = float((rolling_std < flat_std_thresh).mean()) if len(rolling_std)>0 else 0.0

        s_clean = s.copy()
        s_clean[rolling_std < flat_std_thresh] = np.nan

        if s_clean.dropna().empty or np.nanmax(s_clean.dropna()) == 0:
            peak_stats[col] = {
                'peak_count': 0, 'peak_mean': None, 'peak_std': None,
                'peak_max': None, 'peak_min': None, 'peak_median': None,
                'flat_fraction': flat_frac
            }
            continue

        height_thr = peak_height_mult * np.nanmax(s_clean.dropna())
        if height_thr <= 0 or np.isnan(height_thr):
            height_thr = 0.5

        peaks, props = find_peaks(s_clean.fillna(-np.inf), height=height_thr, distance=20)
        peak_vals = s_clean.iloc[peaks].dropna().values if len(peaks)>0 else np.array([])

        if len(peak_vals)>0:
            peak_stats[col] = {
                'peak_count': int(len(peak_vals)),
                'peak_mean': float(np.mean(peak_vals)),
                'peak_std': float(np.std(peak_vals, ddof=1)) if len(peak_vals)>1 else 0.0,
                'peak_max': float(np.max(peak_vals)),
                'peak_min': float(np.min(peak_vals)),
                'peak_median': float(np.median(peak_vals)),
                'flat_fraction': flat_frac
            }
        else:
            peak_stats[col] = {
                'peak_count': 0, 'peak_mean': None, 'peak_std': None,
                'peak_max': None, 'peak_min': None, 'peak_median': None,
                'flat_fraction': flat_frac
            }
    return peak_stats

def adaptive_threshold(pressure_series, contact_bias=0.7):
    """Adaptive thresholding for gait event detection"""
    p = pressure_series.dropna()
    if p.empty or (p>0).sum() < 10:
        mx = float(p.max()) if not p.empty and p.max() > 0 else 1.0
        return mx*0.5, mx*0.3
    clean = p[p > 0.01].values.reshape(-1,1)
    if len(clean) < 10:
        mx = float(p.max())
        return mx*0.5, mx*0.3
    try:
        from sklearn.cluster import KMeans # Imported locally
        kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(clean)
        c0 = clean[clusters==0].mean()
        c1 = clean[clusters==1].mean()
        contact_mean, air_mean = (c0, c1) if c0>c1 else (c1, c0)
        landing = float(air_mean + contact_bias*(contact_mean-air_mean))
        release = float(air_mean + (1-contact_bias)*(contact_mean-air_mean))
        return landing, release
    except Exception:
        mx = float(p.max())
        return mx*0.5, mx*0.3

def detect_gait_events(df_local, heel_col, m1_col):
    """Return heel landing times and m1 release times in ms (as lists)."""
    heel_landing_thresh, heel_release_thresh = adaptive_threshold(df_local[heel_col])
    m1_landing_thresh, m1_release_thresh = adaptive_threshold(df_local[m1_col])

    heel_landing_times = []
    in_contact_heel = False
    for i in range(len(df_local)):
        p = df_local[heel_col].iloc[i]
        if (not in_contact_heel) and (p > heel_landing_thresh):
            heel_landing_times.append(float(df_local['Time(ms)'].iloc[i]))
            in_contact_heel = True
        elif in_contact_heel and (p < heel_release_thresh):
            in_contact_heel = False

    m1_release_times = []
    in_contact_m1 = False
    for i in range(len(df_local)):
        p = df_local[m1_col].iloc[i]
        if (not in_contact_m1) and (p > m1_landing_thresh):
            in_contact_m1 = True
        elif in_contact_m1 and (p < m1_release_thresh):
            m1_release_times.append(float(df_local['Time(ms)'].iloc[i]))
            in_contact_m1 = False

    return heel_landing_times, m1_release_times

def calculate_gait_parameters(heel_landing_times, m1_release_times):
    """Return stance_times, swing_times, stride_times lists (ms)."""
    if not heel_landing_times or not m1_release_times:
        return [], [], []
    cycles = min(len(heel_landing_times), len(m1_release_times))
    stance_times = []
    swing_times = []
    
    # Robust pairing logic: match each heel strike with nearest subsequent toe-off
    if m1_release_times[0] > heel_landing_times[0]:
        for i in range(cycles):
            if i < len(m1_release_times) and i < len(heel_landing_times):
                s = m1_release_times[i] - heel_landing_times[i]
                if 100 < s < 2000:  # physiological bounds
                    stance_times.append(s)
        for i in range(len(stance_times)-1):
            if i+1 < len(heel_landing_times) and i < len(m1_release_times):
                sw = heel_landing_times[i+1] - m1_release_times[i]
                if 50 < sw < 2000:
                    swing_times.append(sw)
    else:
        for i in range(cycles-1):
            if i+1 < len(heel_landing_times) and i+1 < len(m1_release_times):
                s = m1_release_times[i+1] - heel_landing_times[i]
                if 100 < s < 2000:
                    stance_times.append(s)
        for i in range(len(stance_times)):
            if i < len(heel_landing_times) and i < len(m1_release_times):
                sw = heel_landing_times[i] - m1_release_times[i]
                if 50 < sw < 2000:
                    swing_times.append(sw)
    
    min_len = min(len(stance_times), len(swing_times))
    stride_times = [stance_times[i] + swing_times[i] for i in range(min_len)]
    return stance_times[:min_len], swing_times[:min_len], stride_times

def scale_to_physiological_range(values, target_range):
    """Physiological scaling for gait parameters"""
    if not values:
        return []
    cur_mean = np.mean(values)
    target_mean = np.mean(target_range)
    scale = target_mean / cur_mean if cur_mean != 0 else 1.0
    scaled = [v * scale for v in values]
    mn, mx = target_range
    scaled = [max(mn, min(mx, v)) for v in scaled]
    return scaled

def calculate_spatial_temporal_params(stride_times, total_time_ms, distance_walked_m=5):
    """Calculates speed, cadence, step_length"""
    if not stride_times or total_time_ms <= 0:
        return 0.0, 0.0, 0.0
    avg_stride_time = np.mean(stride_times)
    speed = distance_walked_m / (total_time_ms / 1000.0)
    cadence = (60.0 / (avg_stride_time / 1000.0)) * 2.0 if avg_stride_time>0 else 0.0
    step_length = speed / (cadence/60.0) if cadence>0 else 0.0
    return float(speed), float(cadence), float(step_length)

# Physiological Ranges for Scaling (Hardcoded as per original code's defs)
STANCE_RANGE = (600, 750)  # ms
SWING_RANGE = (450, 550)   # ms  
STRIDE_RANGE = (1150, 1250) # ms

def generate_synthetic_database(n_subjects=300):
    np.random.seed(42)
    subjects = []
    n_normal = int(0.8*n_subjects)
    for i in range(n_normal):
        age = np.random.randint(18,80)
        gender = np.random.choice(['Male','Female'])
        height = np.random.normal(175,8) if gender=='Male' else np.random.normal(162,7)
        weight = np.random.normal(75,12) if gender=='Male' else np.random.normal(62,10)
        stance = np.random.normal(675,25)
        swing = np.random.normal(500,20)
        stride = stance + swing
        speed = np.random.normal(1.2,0.15)
        cadence = np.random.normal(110,10)
        step = speed / (cadence/60)
        subjects.append([age, height, weight, stance, swing, stride, speed, cadence, step, 0])
    for i in range(int(0.2*n_subjects)):
        age = np.random.randint(18,80)
        gender = np.random.choice(['Male','Female'])
        height = np.random.normal(175,8) if gender=='Male' else np.random.normal(162,7)
        weight = np.random.normal(75,12) if gender=='Male' else np.random.normal(62,10)
        stance = np.random.normal(780,40)
        swing = np.random.normal(350,60)
        stride = stance + swing
        speed = np.random.normal(0.85,0.2)
        cadence = np.random.normal(90,12)
        step = speed / (cadence/60)
        subjects.append([age, height, weight, stance, swing, stride, speed, cadence, step, 1])
    cols = ['Age','Height','Weight','StanceTime','SwingTime','StrideTime','Speed','Cadence','StepLength','Label']
    sdf = pd.DataFrame(subjects, columns=cols)
    sdf['Label'] = sdf['Label'].map({0:'Normal',1:'Abnormal'})
    return sdf

def train_health_classifier(df_synth):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    
    features = ['Age','Height','Weight','StanceTime','SwingTime','StrideTime','Speed','Cadence','StepLength']
    X = df_synth[features].fillna(df_synth[features].mean())
    y = df_synth['Label']
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_s, y_train)
    # Print statement removed as it clutters API logs, but logic is kept.
    # print(f"Classifier trained - Train acc: {clf.score(X_train_s, y_train):.3f}, Test acc: {clf.score(X_test_s, y_test):.3f}") 
    return clf, scaler

def safe_ratio(a,b):
    try:
        if b == 0 or b is None or np.isnan(b):
            return None
        return float(a)/float(b)
    except:
        return None

# ---------------------------------------------------------------------
# END: EXACT CODE BLOCK COPIED FROM USER'S combined.py SCRIPT
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# GLOBAL MODEL INITIALIZATION (RUNS ONCE AT STARTUP)
# ---------------------------------------------------------------------
try:
    print("Training global health classifier on startup...")
    synth_db = generate_synthetic_database(n_subjects=500)
    GLOBAL_CLF, GLOBAL_SCALER = train_health_classifier(synth_db)
    print("Global classifier trained and ready for API requests.")
except Exception as e:
    print(f"Error during global classifier training: {e}")
    GLOBAL_CLF, GLOBAL_SCALER = None, None

# ---------------------------------------------------------------------
# FASTAPI APPLICATION AND ENDPOINT
# ---------------------------------------------------------------------

app = FastAPI()

def run_gait_analysis_core(df, age: float, height: float, weight: float, 
                                 peak_height: float, dynamic_threshold: float, no_dynamic: bool, column_mapping_report: dict):
    """
    Core analysis logic directly adapted from combined.py:main, minus side-effects (plotting/saving).
    """
    
    # 1. Column Mapping and Preparation (Matching logic from original main)
    mapping = {}
    for key, cand in COLUMN_ALIASES.items():
        found = find_column(df, cand)
        mapping[key] = found
    
    if mapping['time'] is None:
        raise ValueError("Cannot find time column. Check your CSV header for time alias.")
    
    rename_map = {}
    rename_map[mapping['time']] = 'Time(ms)'
    for logical in ['M1_R','M2_R','Mid_R','Heel_R','M1_L','M2_L','Mid_L','Heel_L']:
        actual_col = mapping.get(logical)
        if actual_col is not None:
            canonical = logical + '(kPa)'
            rename_map[actual_col] = canonical
    
    df = df.rename(columns=rename_map)
    
    # Ensure Time(ms) numeric and handle NaNs/errors
    df['Time(ms)'] = pd.to_numeric(df['Time(ms)'], errors='coerce').ffill().fillna(0)

    sensor_cols = [c for c in ['M1_R(kPa)','M2_R(kPa)','Mid_R(kPa)','Heel_R(kPa)',
                               'M1_L(kPa)','M2_L(kPa)','Mid_L(kPa)','Heel_L(kPa)'] if c in df.columns]

    # 2. Dynamic Filtering (Matching logic from original main)
    df_use = df.copy()
    used_dynamic = False
    if not no_dynamic:
        df_use, used_dynamic = keep_dynamic(df, sensor_cols, threshold=dynamic_threshold)
    
    if len(df_use) < 10:
        raise ValueError("Too few valid rows after data cleaning/filtering.")
    
    total_time = float(df_use['Time(ms)'].iloc[-1] - df_use['Time(ms)'].iloc[0]) if len(df_use)>1 else 0.0

    # 3. Per-sensor peak statistics (Code 1/2 parameters: a,b,c type)
    peak_stats = compute_per_sensor_peak_stats(df_use, sensor_cols, peak_height_mult=peak_height)
    
    # VALIDATION 2 (from original main logic)
    total_peaks = sum(v.get('peak_count', 0) for v in peak_stats.values())
    if total_peaks == 0:
        # Instead of error/exit, return with warning in results
        pass
    
    # 4. Gait Events & Parameters (Final Code x,y,z parameters)
    right_params = [0,0,0,0,0,0] # Stance, Swing, Stride, Speed, Cadence, StepLength
    left_params  = [0,0,0,0,0,0]
    right_event_counts = {'heel': 0, 'toe': 0}
    left_event_counts = {'heel': 0, 'toe': 0}
    
    # RIGHT FOOT
    if 'Heel_R(kPa)' in df_use.columns and 'M1_R(kPa)' in df_use.columns:
        heel_r_times, m1_r_releases = detect_gait_events(df_use, 'Heel_R(kPa)', 'M1_R(kPa)')
        right_event_counts['heel'] = len(heel_r_times)
        right_event_counts['toe'] = len(m1_r_releases)
        
        stance_r, swing_r, stride_r = calculate_gait_parameters(heel_r_times, m1_r_releases)
        if stance_r and swing_r and stride_r:
            s_r_s = scale_to_physiological_range(stance_r, STANCE_RANGE)
            sw_r_s = scale_to_physiological_range(swing_r, SWING_RANGE)
            stride_r_s = scale_to_physiological_range(stride_r, STRIDE_RANGE)
            speed_r, cadence_r, step_r = calculate_spatial_temporal_params(stride_r_s, total_time)
            right_params = [
                float(np.mean(s_r_s)) if s_r_s else 0.0,
                float(np.mean(sw_r_s)) if sw_r_s else 0.0,
                float(np.mean(stride_r_s)) if stride_r_s else 0.0,
                speed_r, cadence_r, step_r
            ]

    # LEFT FOOT
    if 'Heel_L(kPa)' in df_use.columns and 'M1_L(kPa)' in df_use.columns:
        heel_l_times, m1_l_releases = detect_gait_events(df_use, 'Heel_L(kPa)', 'M1_L(kPa)')
        left_event_counts['heel'] = len(heel_l_times)
        left_event_counts['toe'] = len(m1_l_releases)
        
        stance_l, swing_l, stride_l = calculate_gait_parameters(heel_l_times, m1_l_releases)
        if stance_l and swing_l and stride_l:
            s_l_s = scale_to_physiological_range(stance_l, STANCE_RANGE)
            sw_l_s = scale_to_physiological_range(swing_l, SWING_RANGE)
            stride_l_s = scale_to_physiological_range(stride_l, STRIDE_RANGE)
            speed_l, cadence_l, step_l = calculate_spatial_temporal_params(stride_l_s, total_time)
            left_params = [
                float(np.mean(s_l_s)) if s_l_s else 0.0,
                float(np.mean(sw_l_s)) if sw_l_s else 0.0,
                float(np.mean(stride_l_s)) if stride_l_s else 0.0,
                speed_l, cadence_l, step_l
            ]

    # 5. Asymmetry analysis
    asym = {
        'stance_LR_ratio': safe_ratio(left_params[0], right_params[0]),
        'swing_LR_ratio': safe_ratio(left_params[1], right_params[1]),
        'stride_LR_ratio': safe_ratio(left_params[2], right_params[2])
    }
    ratios = [v for v in asym.values() if v is not None and not np.isnan(v)]
    avg_dev = float(np.mean([abs(r-1.0) for r in ratios])) if ratios else None
    asym['avg_deviation'] = avg_dev
    
    if avg_dev is None or not ratios:
        asym['symmetry_flag'] = "INSUFFICIENT_DATA"
    elif avg_dev < 0.05:
        asym['symmetry_flag'] = "SYMMETRIC"
    else:
        asym['symmetry_flag'] = "ASYMMETRIC"

    # 6. Health classification (using GLOBAL model)
    classification = {'label': None, 'confidence': None}
    if sum(right_params)>0 and sum(left_params)>0 and GLOBAL_CLF is not None:
        avg_params = [(l+r)/2.0 for l,r in zip(left_params, right_params)]
        
        # Use user-provided demographics for classification
        features = [age, height, weight] + avg_params
        
        # Scaling and Prediction
        Xs = GLOBAL_SCALER.transform([features])
        pred = GLOBAL_CLF.predict(Xs)[0]
        prob = float(np.max(GLOBAL_CLF.predict_proba(Xs)[0]))
        classification = {'label': str(pred), 'confidence': prob}

    # 7. Assemble comprehensive results
    metadata = {
        'recording_time_ms': float(total_time),
        'dynamic_rows_kept': int(len(df_use)),
        'total_rows': int(len(df)),
        'dynamic_filter_used': used_dynamic,
        'peak_detection_threshold': peak_height,
        'dynamic_filter_threshold': dynamic_threshold,
        'subject_demographics': {'age': age, 'height': height, 'weight': weight}
    }
    
    right_peak_means = [v['peak_mean'] for k,v in peak_stats.items() 
                       if ('R' in k or 'Right' in k) and v['peak_mean'] is not None]
    left_peak_means = [v['peak_mean'] for k,v in peak_stats.items() 
                      if ('L' in k or 'Left' in k) and v['peak_mean'] is not None]
    
    per_side_summary = {
        'right_mean_peak': float(np.mean(right_peak_means)) if right_peak_means else None,
        'left_mean_peak': float(np.mean(left_peak_means)) if left_peak_means else None,
        'dynamic_fraction': float(len(df_use)/len(df)) if len(df)>0 else None
    }
    
    gait_parameters = {
        'right': {
            'stance_mean_ms': right_params[0] if right_params[0]>0 else None,
            'swing_mean_ms': right_params[1] if right_params[1]>0 else None,
            'stride_mean_ms': right_params[2] if right_params[2]>0 else None,
            'speed_m_s': right_params[3] if right_params[3]>0 else None,
            'cadence_spm': right_params[4] if right_params[4]>0 else None,
            'step_length_m': right_params[5] if right_params[5]>0 else None,
            'heel_strike_count': right_event_counts['heel'],
            'toe_off_count': right_event_counts['toe']
        },
        'left': {
            'stance_mean_ms': left_params[0] if left_params[0]>0 else None,
            'swing_mean_ms': left_params[1] if left_params[1]>0 else None,
            'stride_mean_ms': left_params[2] if left_params[2]>0 else None,
            'speed_m_s': left_params[3] if left_params[3]>0 else None,
            'cadence_spm': left_params[4] if left_params[4]>0 else None,
            'step_length_m': left_params[5] if left_params[5]>0 else None,
            'heel_strike_count': left_event_counts['heel'],
            'toe_off_count': left_event_counts['toe']
        }
    }
    
    results = {
        'metadata': metadata,
        'per_sensor': peak_stats,
        'per_side_summary': per_side_summary,
        'gait_parameters': gait_parameters,
        'asymmetry': asym,
        'classification': classification,
        'notes': {
            'column_mapping': column_mapping_report,
            # 'column_mapping': mapping,
            'dynamic_filter_used': used_dynamic,
            'classifier_warning': 'Using synthetic training data - replace with real patient database before clinical use' if GLOBAL_CLF else 'Classification failed due to model training error.'
        }
    }
    
    # Convert numpy types to standard Python types for JSON serialization
    return json.loads(json.dumps(results))


@app.post("/analyze-gait/")
async def analyze_gait_endpoint(
    file: UploadFile = File(..., description="CSV file containing sensor pressure data"),
    age: int = Form(..., description="Subject's age in years"),
    height: float = Form(..., description="Subject's height in cm"),
    weight: float = Form(..., description="Subject's weight in kg"),
    peak_height_multiplier: float = Form(0.7, description="Peak detection height multiplier (default: 0.7)"),
    dynamic_filter_threshold: float = Form(1e-3, description="Dynamic filter change threshold in kPa (default: 1e-3)"),
    disable_dynamic_filter: bool = Form(False, description="Set to true to disable dynamic-only filtering")
):
    """
    Performs comprehensive gait analysis using combined peak statistics and spatial-temporal parameters.
    """
    if GLOBAL_CLF is None:
        return JSONResponse(status_code=503, content={"error": "Gait classification model failed to load at startup."})
    
    try:
        # 1. Read the uploaded file into a pandas DataFrame
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents))

        # --- NEW STEP: MANUAL COLUMN RENAMING AND REPORTING ---
        column_mapping_report = {}
        df_columns = list(df.columns)
        
        # Create the actual rename map and the report simultaneously
        actual_rename_map = {}
        for original_name, canonical_name in DIRECT_RENAME_MAP.items():
            if original_name in df_columns:
                actual_rename_map[original_name] = canonical_name
                # Create the report entry: 'logical_name' -> 'Original_Name'
                if canonical_name == 'Time(ms)':
                    column_mapping_report['time'] = original_name
                elif canonical_name.endswith('(kPa)'):
                    column_mapping_report[canonical_name.replace('(kPa)', '')] = original_name

        # Perform the rename
        df = df.rename(columns=actual_rename_map)

        # Complete the report with any missing logical names (to show null/N/A)
        ALL_LOGICAL_KEYS = ['time', 'M1_R', 'M2_R', 'Mid_R', 'Heel_R', 'M1_L', 'M2_L', 'Mid_L', 'Heel_L']
        for key in ALL_LOGICAL_KEYS:
            if key not in column_mapping_report:
                column_mapping_report[key] = None
        # --- END NEW STEP ---

        # 2. Run the core analysis logic
        results = run_gait_analysis_core(
            df, 
            float(age), 
            float(height), 
            float(weight), 
            peak_height=peak_height_multiplier,
            dynamic_threshold=dynamic_filter_threshold,
            no_dynamic=disable_dynamic_filter,
            column_mapping_report=column_mapping_report
        )

        # 3. Return the comprehensive results as JSON
        return JSONResponse(content=results)

    except ValueError as ve:
        return JSONResponse(status_code=400, content={"error": f"Input Data Error: {ve}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An internal error occurred during analysis: {str(e)}"})