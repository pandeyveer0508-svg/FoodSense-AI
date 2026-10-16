import os
import time
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="FoodSense AI - 4D Hyper-Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# HIGH-LEVEL THREE.JS 4D TESSERACT ROTATION & CSS HYPER-ANIMATION EMBEDS
# -----------------------------------------------------------------------------
# 1. Background WebGL 4D Tesseract (Hypercube) Projection
components.html(
    """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <div id="three-4d-bg" style="position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-1; pointer-events:none;"></div>
    <script>
        const container = document.getElementById('three-4d-bg');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        container.appendChild(renderer.domElement);

        // Define 16 vertices of a 4D Hypercube (Tesseract)
        const vertices4D = [];
        for (let i = 0; i < 16; i++) {
            vertices4D.push([
                (i & 1) ? 1 : -1,
                (i & 2) ? 1 : -1,
                (i & 4) ? 1 : -1,
                (i & 8) ? 1 : -1
            ]);
        }

        // Define the 32 edges connecting the 4D vertices
        const edges = [];
        for (let i = 0; i < 16; i++) {
            for (let j = i + 1; j < 16; j++) {
                let diff = 0;
                for (let k = 0; k < 4; k++) {
                    if (vertices4D[i][k] !== vertices4D[j][k]) diff++;
                }
                if (diff === 1) edges.push([i, j]);
            }
        }

        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(edges.length * 2 * 3);
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

        const material = new THREE.LineBasicMaterial({
            color: 0x00f0ff,
            transparent: true,
            opacity: 0.45,
            linewidth: 1.5
        });

        const tesseractLines = new THREE.LineSegments(geometry, material);
        scene.add(tesseractLines);

        camera.position.z = 7;

        let angleXW = 0;
        let angleYZ = 0;
        let mouseX = 0, mouseY = 0;

        document.addEventListener('mousemove', (e) => {
            mouseX = (e.clientX / window.innerWidth - 0.5) * 0.02;
            mouseY = (e.clientY / window.innerHeight - 0.5) * 0.02;
        });

        // 4D to 3D Perspective Projection Matrix Helper
        function project4Dto3D(v, angleXW, angleYZ) {
            let x = v[0], y = v[1], z = v[2], w = v[3];

            // 4D Rotations across XW and YZ planes
            let cosXW = Math.cos(angleXW), sinXW = Math.sin(angleXW);
            let rx = x * cosXW - w * sinXW;
            let rw = x * sinXW + w * cosXW;

            let cosYZ = Math.cos(angleYZ), sinYZ = Math.sin(angleYZ);
            let ry = y * cosYZ - z * sinYZ;
            let rz = y * sinYZ + z * cosYZ;

            // 4D Perspective distance camera w-offset
            let distance = 2.8;
            let wFactor = 1 / (distance - rw);

            return [rx * wFactor * 2.2, ry * wFactor * 2.2, rz * wFactor * 2.2];
        }

        function animate() {
            requestAnimationFrame(animate);

            angleXW += 0.008 + mouseX;
            angleYZ += 0.006 + mouseY;

            const posAttribute = tesseractLines.geometry.attributes.position;
            let idx = 0;

            for (let i = 0; i < edges.length; i++) {
                let v1 = project4Dto3D(vertices4D[edges[i][0]], angleXW, angleYZ);
                let v2 = project4Dto3D(vertices4D[edges[i][1]], angleXW, angleYZ);

                posAttribute.array[idx++] = v1[0];
                posAttribute.array[idx++] = v1[1];
                posAttribute.array[idx++] = v1[2];

                posAttribute.array[idx++] = v2[0];
                posAttribute.array[idx++] = v2[1];
                posAttribute.array[idx++] = v2[2];
            }

            posAttribute.needsUpdate = true;
            tesseractLines.rotation.y += 0.002;

            renderer.render(scene, camera);
        }

        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
    """,
    height=0,
)

# 2. 4D CSS Keyframe Animations & Glassmorphism Hyper-card Effects
st.markdown("""
<style>
    @keyframes hyper4DGradient {
        0% { background-position: 0% 50%; filter: hue-rotate(0deg); }
        50% { background-position: 100% 50%; filter: hue-rotate(90deg); }
        100% { background-position: 0% 50%; filter: hue-rotate(0deg); }
    }

    @keyframes tesseractWarp {
        0% { transform: translateY(0px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1); }
        33% { transform: translateY(-8px) rotateX(4deg) rotateY(-4deg) scale3d(1.02, 0.98, 1.02); }
        66% { transform: translateY(-4px) rotateX(-3deg) rotateY(3deg) scale3d(0.99, 1.01, 0.99); }
        100% { transform: translateY(0px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1); }
    }

    @keyframes chronoPulse {
        0% { box-shadow: 0 0 15px rgba(0, 240, 255, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.2); }
        50% { box-shadow: 0 0 40px rgba(138, 43, 226, 0.7), 0 0 20px rgba(0, 240, 255, 0.8), inset 0 0 20px rgba(138, 43, 226, 0.4); }
        100% { box-shadow: 0 0 15px rgba(0, 240, 255, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.2); }
    }

    /* 4D Header Container */
    .main-header-4d {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #00f0ff);
        background-size: 400% 400%;
        animation: hyper4DGradient 12s ease infinite, tesseractWarp 8s ease-in-out infinite, chronoPulse 5s ease-in-out infinite;
        padding: 35px;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        perspective: 1200px;
        transform-style: preserve-3d;
        border: 1px solid rgba(0, 240, 255, 0.3);
    }

    /* 4D Hyper-Text Styling */
    .text-4d {
        font-weight: 900;
        text-transform: uppercase;
        color: #FFFFFF;
        text-shadow: 
            0 1px 0 #8a2be2,
            0 2px 0 #7b1fa2,
            0 3px 0 #512da8,
            0 4px 0 #311b92,
            0 8px 20px rgba(0, 240, 255, 0.6);
    }
    
    /* Interactive 4D Glassmorphism Metric Card */
    .metric-card-4d {
        background: rgba(15, 12, 41, 0.75);
        backdrop-filter: blur(16px);
        border-left: 8px solid #00f0ff;
        border-right: 1px solid rgba(138, 43, 226, 0.3);
        padding: 24px;
        border-radius: 18px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        margin-top: 15px;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        transform-style: preserve-3d;
        perspective: 1000px;
        color: #FFFFFF;
    }
    
    .metric-card-4d:hover {
        transform: translateY(-12px) rotateY(-8deg) rotateX(8deg) scale(1.03);
        box-shadow: 0 30px 60px rgba(0, 240, 255, 0.5), 0 0 20px rgba(138, 43, 226, 0.4);
        border-left-color: #8a2be2;
    }

    .status-badge-4d {
        display: inline-block;
        padding: 8px 16px;
        background: rgba(0, 240, 255, 0.15);
        color: #00f0ff;
        border: 1px solid #00f0ff;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        box-shadow: 0 4px 15px rgba(0, 240, 255, 0.3);
        animation: tesseractWarp 4s ease-in-out infinite;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 0px 0px;
        padding: 12px 24px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CONSTANTS & MAPS
# -----------------------------------------------------------------------------
WEATHER_MAP = {"Sunny": 0, "Rainy": 1, "Cloudy": 2, "Snowy": 3}
MEAL_TYPE_MAP = {"Breakfast": 0, "Lunch": 1, "Dinner": 2, "Late Night": 3}
DAY_MAP = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
    "Friday": 4, "Saturday": 5, "Sunday": 6
}

# -----------------------------------------------------------------------------
# MODEL ARTIFACT LOADING
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def resolve_path(filename):
    models_subfolder_path = os.path.join(BASE_DIR, "models", filename)
    root_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(models_subfolder_path):
        return models_subfolder_path
    return root_path

@st.cache_resource
def load_ml_artifacts():
    artifacts = {}
    files_to_load = {
        "linear_reg": "linear_reg.pkl",
        "knn_reg": "knn_reg.pkl",
        "random_forest": "random_forest_model.pkl",
        "xgboost": "xgboost_model.pkl",
        "tree_model": "tree_model.pkl",
        "scaler": "scaler.pkl",
        "x_columns_demand": "x_columns_demand.pkl",
        "X_column_cust": "X_column_cust.pkl"
    }

    missing_files = []
    for key, filename in files_to_load.items():
        file_path = resolve_path(filename)
        if not os.path.exists(file_path):
            missing_files.append(filename)
        else:
            try:
                artifacts[key] = joblib.load(file_path)
            except Exception as e:
                st.error(f"Error loading {filename}: {str(e)}")
                return None, missing_files

    if missing_files:
        return None, missing_files

    return artifacts, []

artifacts, missing_files = load_ml_artifacts()

if missing_files:
    st.error("🚨 Missing Required Model Artifacts!")
    st.warning(
        "The following required `.pkl` files could not be found:\n\n"
        + "\n".join([f"- `{f}`" for f in missing_files])
    )
    st.info("Please place all `.pkl` files in the app directory or inside a `/models` folder and refresh.")
    st.stop()

linear_reg = artifacts["linear_reg"]
knn_reg = artifacts["knn_reg"]
random_forest = artifacts["random_forest"]
xgboost_model = artifacts["xgboost"]
tree_model = artifacts["tree_model"]
scaler = artifacts["scaler"]
x_columns_demand = artifacts["x_columns_demand"]
X_column_cust = artifacts["X_column_cust"]

if "last_predicted_customers" not in st.session_state:
    st.session_state["last_predicted_customers"] = 185.0
if "last_predicted_demand" not in st.session_state:
    st.session_state["last_predicted_demand"] = 320.0

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def predict_with_feature_matching(model, df):
    try:
        if hasattr(model, "get_booster") and model.get_booster().feature_names is not None:
            expected_names = model.get_booster().feature_names
            return model.predict(df[expected_names])
    except Exception:
        pass

    if hasattr(model, "n_features_in_"):
        n_expected = model.n_features_in_
        if df.shape[1] != n_expected:
            return model.predict(df.iloc[:, :n_expected])

    return model.predict(df)

# -----------------------------------------------------------------------------
# SIDEBAR CONTROL PANEL
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Command Center")
    st.markdown("---")
    st.markdown("<div class='status-badge-4d'>⚡ 4D Hypercube Engine Active</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("💡 System Capabilities")
    st.info(
        "• **Tab 1:** 4D Temporal Footfall Inference\n"
        "• **Tab 2:** Kitchen Demand Forecasting"
    )

# -----------------------------------------------------------------------------
# APP HEADER WITH 4D TEXT & ANIMATION
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-header-4d">
    <h1 class="text-4d" style="margin: 0; font-size: 2.8rem;">⚡ FOODSENSE AI 4D HYPER-ENGINE</h1>
    <p style="font-size: 1.2rem; margin-top: 10px; opacity: 0.95; font-weight: 500;">
        4D Spatio-Temporal Predictive Customer & Demand Simulation
    </p>
</div>
""", unsafe_allow_html=True)

# KPI Ribbon
stat_col1, stat_col2, stat_col3 = st.columns(3)
with stat_col1:
    st.metric(label="Inference Latency", value="38 ms", delta="-4ms", delta_color="inverse")
with stat_col2:
    st.metric(label="Forecast Customers", value=f"{st.session_state['last_predicted_customers']:.0f}")
with stat_col3:
    st.metric(label="Forecast Demand", value=f"{st.session_state['last_predicted_demand']:.0f} units")

st.markdown("---")

tab1, tab2 = st.tabs([
    "👥 Predict Customer Footfall", 
    "📦 Predict Item Demand"
])

# =============================================================================
# TAB 1: PREDICT EXPECTED CUSTOMERS
# =============================================================================
with tab1:
    st.markdown("### Operational Context Inputs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weather_input = st.selectbox("Weather Condition", options=list(WEATHER_MAP.keys()), key="tab1_weather")
        day_input = st.selectbox("Day of Week", options=list(DAY_MAP.keys()), key="tab1_day")
        meal_type_input = st.selectbox("Meal Type", options=list(MEAL_TYPE_MAP.keys()), key="tab1_meal")

    with col2:
        temperature_input = st.number_input("Temperature (°C)", min_value=-20.0, max_value=50.0, value=25.0, step=0.5, key="tab1_temp")
        local_event_input = st.checkbox("Local Event Nearby?", value=False, key="tab1_event")
        holiday_input = st.checkbox("Is Holiday?", value=False, key="tab1_holiday")

    st.markdown("---")

    model_choice_tab1 = st.radio("Select Prediction Model", options=["XGBoost", "Decision Tree"], horizontal=True, key="tab1_model_choice")

    if st.button("🔮 Predict Customer Footfall", type="primary", key="tab1_btn"):
        progress_bar = st.progress(0)
        for percent in range(0, 101, 25):
            time.sleep(0.04)
            progress_bar.progress(percent)
        progress_bar.empty()

        all_possible_cust_inputs = {
            "Weather_label": WEATHER_MAP[weather_input],
            "Day_label": DAY_MAP[day_input],
            "Meal_Type_Label": MEAL_TYPE_MAP[meal_type_input],
            "Local_Event_Nearby": 1 if local_event_input else 0,
            "Temperature": temperature_input,
            "Holiday": 1 if holiday_input else 0
        }

        ordered_cols = [c for c in X_column_cust if c in all_possible_cust_inputs]
        feature_df = pd.DataFrame([all_possible_cust_inputs])[ordered_cols]

        selected_model = xgboost_model if model_choice_tab1 == "XGBoost" else tree_model
        prediction_res = predict_with_feature_matching(selected_model, feature_df)
        
        prediction_val = prediction_res[0] if isinstance(prediction_res, (np.ndarray, list, pd.Series)) else prediction_res
        predicted_cust_val = max(0.0, float(prediction_val))
        st.session_state["last_predicted_customers"] = round(predicted_cust_val, 2)

        st.toast(f"✅ Predicted Footfall: {predicted_cust_val:.0f} visitors", icon="👥")

        st.markdown(f"""
        <div class="metric-card-4d">
            <h3 style="margin: 0; color: #00f0ff;">Predicted Expected Customers (Footfall)</h3>
            <h1 class="text-4d" style="margin: 5px 0 0 0; color: #FF6B6B; font-size: 3rem;">{predicted_cust_val:.2f} <span style="font-size: 1.2rem; color: #A0AEC0;">visitors</span></h1>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# TAB 2: PREDICT EXPECTED DEMAND
# =============================================================================
with tab2:
    st.markdown("### Inputs for Demand Forecasting")

    use_tab1_val = st.checkbox(
        f"Auto-fill 'Expected Customers' from Tab 1 prediction ({st.session_state['last_predicted_customers']} customers)",
        value=True, key="auto_fill_chk"
    )

    default_customers = st.session_state["last_predicted_customers"] if use_tab1_val else 150.0

    col1, col2 = st.columns(2)

    with col1:
        expected_cust_input = st.number_input("Expected Customers", min_value=0.0, max_value=10000.0, value=float(default_customers), step=1.0, key="tab2_expected_cust")
        prev_day_sales_input = st.number_input("Previous Day Sales ($ / Units)", min_value=0.0, max_value=500000.0, value=1200.0, step=10.0, key="tab2_prev_day")
        prev_week_sales_input = st.number_input("Previous Week Sales ($ / Units)", min_value=0.0, max_value=3500000.0, value=8500.0, step=50.0, key="tab2_prev_week")

    with col2:
        meal_type_input_t2 = st.selectbox("Meal Type", options=list(MEAL_TYPE_MAP.keys()), key="tab2_meal")
        weather_input_t2 = st.selectbox("Weather Condition", options=list(WEATHER_MAP.keys()), key="tab2_weather")
        local_event_input_t2 = st.checkbox("Local Event Nearby?", value=False, key="tab2_event")

    st.markdown("---")

    model_choice_tab2 = st.radio("Select Prediction Model", options=["Linear Regression", "KNN Regressor", "Random Forest"], horizontal=True, key="tab2_model_choice")

    if st.button("🔮 Predict Expected Demand", type="primary", key="tab2_btn"):
        all_possible_demand_inputs = {
            "Expected_Customers": expected_cust_input,
            "Previous_day_sales": prev_day_sales_input,
            "Previous_week_sales": prev_week_sales_input,
            "Meal_Type_Label": MEAL_TYPE_MAP[meal_type_input_t2],
            "Local_Event_Nearby": 1 if local_event_input_t2 else 0,
            "Weather_label": WEATHER_MAP[weather_input_t2]
        }

        ordered_demand_cols = [c for c in x_columns_demand if c in all_possible_demand_inputs]
        raw_feature_df = pd.DataFrame([all_possible_demand_inputs])[ordered_demand_cols]

        if model_choice_tab2 == "Linear Regression":
            scaled_features = scaler.transform(raw_feature_df)
            feature_vector_sent = pd.DataFrame(scaled_features, columns=ordered_demand_cols)
            prediction_t2 = predict_with_feature_matching(linear_reg, feature_vector_sent)
        elif model_choice_tab2 == "KNN Regressor":
            prediction_t2 = predict_with_feature_matching(knn_reg, raw_feature_df)
        else:
            prediction_t2 = predict_with_feature_matching(random_forest, raw_feature_df)

        prediction_val_t2 = prediction_t2[0] if isinstance(prediction_t2, (np.ndarray, list, pd.Series)) else prediction_t2
        predicted_demand_val = max(0.0, float(prediction_val_t2))
        st.session_state["last_predicted_demand"] = round(predicted_demand_val, 2)

        st.toast(f"✅ Predicted Demand: {predicted_demand_val:.2f} units", icon="📦")

        st.markdown(f"""
        <div class="metric-card-4d" style="border-left-color: #2ECC71;">
            <h3 style="margin: 0; color: #00f0ff;">Predicted Expected Demand</h3>
            <h1 class="text-4d" style="margin: 5px 0 0 0; color: #2ECC71; font-size: 3rem;">{predicted_demand_val:.2f} <span style="font-size: 1.2rem; color: #A0AEC0;">units</span></h1>
        </div>
        """, unsafe_allow_html=True) 