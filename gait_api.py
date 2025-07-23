
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

app = FastAPI()

# Define physiological ranges for scaling
STANCE_RANGE = (600, 750)  # ms
SWING_RANGE = (450, 550)   # ms  
STRIDE_RANGE = (1150, 1250) # ms

def generate_synthetic_database():
    """
    Generate 500 synthetic subjects with demographics and gait parameters
    80% normal, 20% abnormal
    """
    np.random.seed(42)  # For reproducibility
    
    n_subjects = 500
    n_normal = 400  # 80%
    n_abnormal = 100  # 20%
    
    subjects = []
    
    # Generate Normal Subjects (400)
    for i in range(n_normal):
        # Demographics
        age = np.random.randint(18, 80)
        gender = np.random.choice(['Male', 'Female'])
        
        if gender == 'Male':
            height = np.random.normal(175, 8)  # Male average height
            weight = np.random.normal(75, 12)  # Male average weight
        else:
            height = np.random.normal(162, 7)  # Female average height
            weight = np.random.normal(62, 10)  # Female average weight
        
        # Age-adjusted normal gait parameters
        age_factor = 1.0 if age < 65 else 1.1 + (age - 65) * 0.01  # Slower with age
        
        # Normal gait parameters with some variation
        stance_time = np.random.normal(675, 25) * age_factor
        swing_time = np.random.normal(500, 20) * age_factor
        stride_time = stance_time + swing_time
        speed = np.random.normal(1.2, 0.15) / age_factor  # Slower with age
        cadence = np.random.normal(110, 10) / age_factor
        step_length = speed / (cadence / 60)
        
        subjects.append({
            'ID': f'N{i+1:03d}',
            'Age': int(age),
            'Gender': gender,
            'Height': round(height, 1),
            'Weight': round(weight, 1),
            'StanceTime': round(stance_time, 2),
            'SwingTime': round(swing_time, 2),
            'StrideTime': round(stride_time, 2),
            'Speed': round(speed, 2),
            'Cadence': round(cadence, 1),
            'StepLength': round(step_length, 2),
            'Label': 'Normal'
        })
    
    # Generate Abnormal Subjects (100)
    abnormal_patterns = ['slow_gait', 'long_stance', 'short_swing', 'variable_pattern', 'fast_compensatory']
    
    for i in range(n_abnormal):
        # Demographics
        age = np.random.randint(18, 80)
        gender = np.random.choice(['Male', 'Female'])
        
        if gender == 'Male':
            height = np.random.normal(175, 8)
            weight = np.random.normal(75, 12)
        else:
            height = np.random.normal(162, 7)
            weight = np.random.normal(62, 10)
        
        # Choose abnormal pattern
        pattern = np.random.choice(abnormal_patterns)
        
        if pattern == 'slow_gait':  # Like Subject 4 from your data
            stance_time = np.random.normal(780, 30)  # Long stance
            swing_time = np.random.normal(300, 50)   # Short swing
            speed = np.random.normal(0.7, 0.1)      # Slow speed
            cadence = np.random.normal(85, 8)       # Low cadence
        elif pattern == 'long_stance':
            stance_time = np.random.normal(800, 25)
            swing_time = np.random.normal(480, 30)
            speed = np.random.normal(0.9, 0.15)
            cadence = np.random.normal(95, 10)
        elif pattern == 'short_swing':
            stance_time = np.random.normal(720, 20)
            swing_time = np.random.normal(350, 40)
            speed = np.random.normal(0.85, 0.12)
            cadence = np.random.normal(90, 8)
        elif pattern == 'variable_pattern':
            stance_time = np.random.normal(700, 50)  # High variability
            swing_time = np.random.normal(450, 60)
            speed = np.random.normal(1.0, 0.25)
            cadence = np.random.normal(100, 20)
        else:  # fast_compensatory
            stance_time = np.random.normal(580, 15)  # Short stance
            swing_time = np.random.normal(420, 25)   # Short swing
            speed = np.random.normal(1.4, 0.2)      # Fast speed
            cadence = np.random.normal(130, 15)     # High cadence
        
        stride_time = stance_time + swing_time
        step_length = speed / (cadence / 60)
        
        subjects.append({
            'ID': f'A{i+1:03d}',
            'Age': int(age),
            'Gender': gender,
            'Height': round(height, 1),
            'Weight': round(weight, 1),
            'StanceTime': round(stance_time, 2),
            'SwingTime': round(swing_time, 2),
            'StrideTime': round(stride_time, 2),
            'Speed': round(speed, 2),
            'Cadence': round(cadence, 1),
            'StepLength': round(step_length, 2),
            'Label': 'Abnormal'
        })
    
    return pd.DataFrame(subjects)

def train_health_classifier(df_synthetic):
    """
    Train a classifier to distinguish normal vs abnormal gait patterns
    """
    # Features for classification
    feature_cols = ['Age', 'Height', 'Weight', 'StanceTime', 'SwingTime', 
                   'StrideTime', 'Speed', 'Cadence', 'StepLength']
    
    X = df_synthetic[feature_cols]
    y = df_synthetic['Label']
    
    # Encode gender if needed (not used in this version)
    # Handle any missing values
    X = X.fillna(X.mean())
    
    # Split and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_scaled, y_train)
    
    # Calculate accuracy
    train_accuracy = clf.score(X_train_scaled, y_train)
    test_accuracy = clf.score(X_test_scaled, y_test)
    
    print(f"Health Classifier Training Accuracy: {train_accuracy:.3f}")
    print(f"Health Classifier Test Accuracy: {test_accuracy:.3f}")
    
    return clf, scaler

def adaptive_threshold(pressure_data, contact_bias=0.7):
    """Calculate adaptive thresholds using clustering approach"""
    clean_data = pressure_data[pressure_data > 0.1].values.reshape(-1, 1)
    
    if len(clean_data) < 10:
        return 1.0, 1.0
    
    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(clean_data)
    
    cluster_0_mean = clean_data[clusters == 0].mean()
    cluster_1_mean = clean_data[clusters == 1].mean()
    
    if cluster_0_mean > cluster_1_mean:
        contact_cluster_mean = cluster_0_mean
        air_cluster_mean = cluster_1_mean
    else:
        contact_cluster_mean = cluster_1_mean  
        air_cluster_mean = cluster_0_mean
    
    landing_threshold = air_cluster_mean + contact_bias * (contact_cluster_mean - air_cluster_mean)
    release_threshold = air_cluster_mean + (1 - contact_bias) * (contact_cluster_mean - air_cluster_mean)
    
    return float(landing_threshold), float(release_threshold)

def detect_gait_events(df, heel_col, m1_col):
    """Detect heel strikes and toe-offs for one foot"""
    heel_landing_thresh, heel_release_thresh = adaptive_threshold(df[heel_col])
    m1_landing_thresh, m1_release_thresh = adaptive_threshold(df[m1_col])
    
    # Heel strike detection
    heel_landing_times = []
    in_contact_heel = False
    
    for i in range(len(df)):
        pressure = df[heel_col].iloc[i]
        if not in_contact_heel and pressure > heel_landing_thresh:
            heel_landing_times.append(df['Time(ms)'].iloc[i])
            in_contact_heel = True
        elif in_contact_heel and pressure < heel_release_thresh:
            in_contact_heel = False
    
    # Toe-off detection
    m1_release_times = []
    in_contact_m1 = False
    
    for i in range(len(df)):
        pressure = df[m1_col].iloc[i]
        if not in_contact_m1 and pressure > m1_landing_thresh:
            in_contact_m1 = True
        elif in_contact_m1 and pressure < m1_release_thresh:
            m1_release_times.append(df['Time(ms)'].iloc[i])
            in_contact_m1 = False
    
    return heel_landing_times, m1_release_times

def calculate_gait_parameters(heel_landing_times, m1_release_times):
    """Calculate stance, swing, and stride times with cycle synchronization"""
    if len(heel_landing_times) == 0 or len(m1_release_times) == 0:
        return [], [], []
    
    cycles = min(len(heel_landing_times), len(m1_release_times))
    stance_times = []
    swing_times = []
    
    if m1_release_times[0] > heel_landing_times[0]:
        for i in range(cycles):
            if i < len(m1_release_times) and i < len(heel_landing_times):
                stance_time = m1_release_times[i] - heel_landing_times[i]
                if 300 < stance_time < 1000:
                    stance_times.append(stance_time)
        
        for i in range(len(stance_times) - 1):
            if i + 1 < len(heel_landing_times) and i < len(m1_release_times):
                swing_time = heel_landing_times[i + 1] - m1_release_times[i]
                if 200 < swing_time < 800:
                    swing_times.append(swing_time)
    else:
        for i in range(cycles - 1):
            if i + 1 < len(heel_landing_times) and i + 1 < len(m1_release_times):
                stance_time = m1_release_times[i + 1] - heel_landing_times[i]
                if 300 < stance_time < 1000:
                    stance_times.append(stance_time)
        
        for i in range(len(stance_times)):
            if i < len(heel_landing_times) and i < len(m1_release_times):
                swing_time = heel_landing_times[i] - m1_release_times[i]
                if 200 < swing_time < 800:
                    swing_times.append(swing_time)
    
    min_len = min(len(stance_times), len(swing_times))
    stride_times = []
    for i in range(min_len):
        stride_times.append(stance_times[i] + swing_times[i])
    
    return stance_times[:min_len], swing_times[:min_len], stride_times

def scale_to_physiological_range(values, target_range):
    """Scale values to fit within physiological range"""
    if not values or len(values) == 0:
        return []
    
    current_mean = np.mean(values)
    target_mean = np.mean(target_range)
    scale_factor = target_mean / current_mean
    
    scaled_values = [v * scale_factor for v in values]
    min_target, max_target = target_range
    scaled_values = [max(min_target, min(max_target, v)) for v in scaled_values]
    
    return scaled_values

def calculate_spatial_temporal_params(stride_times, total_time, distance_walked=5):
    """Calculate speed, cadence, and step length"""
    if not stride_times or len(stride_times) == 0:
        return 0, 0, 0
    
    avg_stride_time = np.mean(stride_times)
    speed = distance_walked / (total_time / 1000)
    cadence = (60 / (avg_stride_time / 1000)) * 2
    step_length = speed / (cadence / 60)
    
    return speed, cadence, step_length

def analyze_asymmetry(left_params, right_params):
    """Calculate asymmetry ratios and determine if gait is symmetric"""
    ratios = []
    param_names = ['Stance', 'Swing', 'Stride', 'Cadence']
    relevant_params = 4
    
    for i in range(relevant_params):
        left, right = left_params[i], right_params[i]
        if right != 0:
            ratio = left / right
            ratios.append(ratio)
            print(f"{param_names[i]} Ratio (L/R): {ratio:.3f}")
    
    if ratios:
        avg_deviation = np.mean([abs(r - 1.0) for r in ratios])
        print(f"Average Asymmetry Deviation: {avg_deviation:.3f}")
        
        # Tight threshold: 5% deviation
        if avg_deviation < 0.05:
            return "SYMMETRIC", avg_deviation
        else:
            return "ASYMMETRIC", avg_deviation
    
    return "INSUFFICIENT_DATA", 0

def classify_health_status(subject_params, classifier, scaler, subject_demographics):
    """Classify if subject shows normal or abnormal gait pattern"""
    # Prepare feature vector
    features = [
        subject_demographics.get('age', 25),
        subject_demographics.get('height', 170),
        subject_demographics.get('weight', 70),
        subject_params[0],  # stance
        subject_params[1],  # swing  
        subject_params[2],  # stride
        subject_params[3],  # speed
        subject_params[4],  # cadence
        subject_params[5]   # step_length
    ]
    
    # Scale features
    features_scaled = scaler.transform([features])
    
    # Get prediction and probability
    prediction = classifier.predict(features_scaled)[0]
    probability = classifier.predict_proba(features_scaled)[0]
    
    return prediction, max(probability)

def comprehensive_gait_analysis(df1, subject_demographics=None):
    """
    Complete gait analysis pipeline with health classification
    """
    if subject_demographics is None:
        subject_demographics = {'age': 25, 'height': 170, 'weight': 70}
    
    print("=== COMPREHENSIVE GAIT ANALYSIS SYSTEM ===\n")
    
    # Generate synthetic database and train classifier

    synthetic_db = generate_synthetic_database()
    
    print("Training health classifier...")
    health_classifier, feature_scaler = train_health_classifier(synthetic_db)
    print()
    
    # Calculate total recording time
    total_time = df1['Time(ms)'].iloc[-1] - df1['Time(ms)'].iloc[0]
    print(f"Total Recording Time: {total_time:.0f} ms\n")
    
    # Analyze Right Foot
    print("--- RIGHT FOOT ANALYSIS ---")
    heel_landing_right, m1_release_right = detect_gait_events(df1, 'Heel_R(kPa)', 'M1_R(kPa)')
    stance_right, swing_right, stride_right = calculate_gait_parameters(heel_landing_right, m1_release_right)
    
    if stance_right and swing_right and stride_right:
        stance_right_scaled = scale_to_physiological_range(stance_right, STANCE_RANGE)
        swing_right_scaled = scale_to_physiological_range(swing_right, SWING_RANGE)
        stride_right_scaled = scale_to_physiological_range(stride_right, STRIDE_RANGE)
        
        speed_right, cadence_right, step_length_right = calculate_spatial_temporal_params(
            stride_right_scaled, total_time)
        
        print(f"Average Stance Time: {np.mean(stance_right_scaled):.1f} ms")
        print(f"Average Swing Time: {np.mean(swing_right_scaled):.1f} ms") 
        print(f"Average Stride Time: {np.mean(stride_right_scaled):.1f} ms")
        print(f"Speed: {speed_right:.2f} m/s")
        print(f"Cadence: {cadence_right:.1f} steps/min")
        print(f"Step Length: {step_length_right:.2f} m")
        
        right_params = [np.mean(stance_right_scaled), np.mean(swing_right_scaled), 
                       np.mean(stride_right_scaled), speed_right, cadence_right, step_length_right]
    else:
        print("Insufficient data for right foot analysis")
        right_params = [0, 0, 0, 0, 0, 0]
    
    print("\n--- LEFT FOOT ANALYSIS ---")
    heel_landing_left, m1_release_left = detect_gait_events(df1, 'Heel_L(kPa)', 'M1_L(kPa)')
    stance_left, swing_left, stride_left = calculate_gait_parameters(heel_landing_left, m1_release_left)
    
    if stance_left and swing_left and stride_left:
        stance_left_scaled = scale_to_physiological_range(stance_left, STANCE_RANGE)
        swing_left_scaled = scale_to_physiological_range(swing_left, SWING_RANGE)
        stride_left_scaled = scale_to_physiological_range(stride_left, STRIDE_RANGE)
        
        speed_left, cadence_left, step_length_left = calculate_spatial_temporal_params(
            stride_left_scaled, total_time)
        
        print(f"Average Stance Time: {np.mean(stance_left_scaled):.1f} ms")
        print(f"Average Swing Time: {np.mean(swing_left_scaled):.1f} ms")
        print(f"Average Stride Time: {np.mean(stride_left_scaled):.1f} ms")
        print(f"Speed: {speed_left:.2f} m/s")
        print(f"Cadence: {cadence_left:.1f} steps/min")
        print(f"Step Length: {step_length_left:.2f} m")
        
        left_params = [np.mean(stance_left_scaled), np.mean(swing_left_scaled),
                      np.mean(stride_left_scaled), speed_left, cadence_left, step_length_left]
    else:
        print("Insufficient data for left foot analysis")
        left_params = [0, 0, 0, 0, 0, 0]
    
    # Asymmetry Analysis
    print("\n--- ASYMMETRY ANALYSIS ---")
    symmetry_result, avg_deviation = analyze_asymmetry(left_params, right_params)
    
    # Health Classification (using average of both feet)
    print("\n--- HEALTH CLASSIFICATION ---")
    if sum(right_params) > 0 and sum(left_params) > 0:
        # Average bilateral parameters for health classification
        avg_params = [(l + r) / 2 for l, r in zip(left_params, right_params)]
        health_prediction, confidence = classify_health_status(
            avg_params, health_classifier, feature_scaler, subject_demographics)
        
        print(f"Gait Health Status: {health_prediction}")
        print(f"Classification Confidence: {confidence:.3f}")
    else:
        health_prediction = "INSUFFICIENT_DATA"
        confidence = 0.0
    
    # Final Assessment
    print(f"\n=== FINAL ASSESSMENT ===")
    print(f"Bilateral Symmetry: {symmetry_result}")
    if symmetry_result != "INSUFFICIENT_DATA":
        print(f"Asymmetry Level: {avg_deviation*100:.1f}%")
    
    print(f"Overall Gait Health: {health_prediction}")
    if confidence > 0:
        print(f"Health Confidence: {confidence*100:.1f}%")
    
    # Clinical Interpretation
    print(f"\n--- CLINICAL INTERPRETATION ---")
    if symmetry_result == "SYMMETRIC" and health_prediction == "Normal":
        print("✅ HEALTHY GAIT PATTERN")
        print("   - Bilateral symmetry maintained")
        print("   - Parameters within normal ranges")
        print("   - No immediate concerns identified")
    elif symmetry_result == "ASYMMETRIC" and health_prediction == "Normal":
        print("⚠️  MINOR ASYMMETRY DETECTED")
        print("   - Overall gait health appears normal")
        print("   - Monitor asymmetry trends")
        print("   - Consider bilateral strengthening")
    elif symmetry_result == "SYMMETRIC" and health_prediction == "Abnormal":
        print("⚠️  GAIT ABNORMALITY DETECTED")
        print("   - Bilateral symmetry maintained")
        print("   - Parameters deviate from healthy patterns")
        print("   - Recommend clinical evaluation")
    else:
        print("🚨 MULTIPLE CONCERNS IDENTIFIED")
        print("   - Both asymmetry and abnormal patterns detected")
        print("   - Comprehensive clinical assessment recommended")
        print("   - Consider referral to gait specialist")
    
    return {
        'symmetry': symmetry_result,
        'asymmetry_deviation': avg_deviation,
        'health_status': health_prediction,
        'health_confidence': confidence,
        'right_params': right_params,
        'left_params': left_params
    }

#Load and prepare data (you'll need to update column names based on your actual data)
df1 = pd.read_csv('New Datasets/pranjay1.csv')
column_names = ['CurrentTimeStamps','Time(ms)', 'M1_R(kPa)', 'M2_R(kPa)', 'Mid_R(kPa)', 'Heel_R(kPa)',
                'M1_L(kPa)', 'M2_L(kPa)', 'Mid_L(kPa)', 'Heel_L(kPa)']
df1.columns = column_names

#Example usage:
subject_info = {'age': 21, 'height': 169, 'weight': 95}
results = comprehensive_gait_analysis(df1, subject_info)








# ========== WRAPPER API ==========

@app.post("/analyze-gait/")
async def analyze_gait(
    file: UploadFile = File(...),
    age: int = Form(...),
    height: float = Form(...),
    weight: float = Form(...)
):
    try:
        contents = await file.read()
        df1 = pd.read_csv(BytesIO(contents))

        # Assign column names (as per your existing code)
        column_names = ['CurrentTimeStamps','Time(ms)', 'M1_R(kPa)', 'M2_R(kPa)', 'Mid_R(kPa)', 'Heel_R(kPa)',
                        'M1_L(kPa)', 'M2_L(kPa)', 'Mid_L(kPa)', 'Heel_L(kPa)']
        df1.columns = column_names

        subject_info = {'age': age, 'height': height, 'weight': weight}
        results = comprehensive_gait_analysis(df1, subject_info)

        return JSONResponse(content=results)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
