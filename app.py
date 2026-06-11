import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time
import os

# --- STYLING & PAGE INITIALIZATION ---
st.set_page_config(
    page_title="Ottawa Summer Camp Planner",
    page_icon="⛺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject modern Google Font and sleek custom CSS styles for premium visuals
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    /* Global font override */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Modern Glassmorphic Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: #0d9488;
    }
    .metric-title {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.875rem;
        color: #0f172a;
        font-weight: 700;
        line-height: 1.25;
    }
    .metric-subtitle {
        font-size: 0.875rem;
        color: #0d9488;
        font-weight: 500;
        margin-top: 4px;
    }
    
    /* Header Gradient & Animation */
    .gradient-header {
        background: linear-gradient(135deg, #0f172a 0%, #0d9488 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.75rem;
        margin-bottom: 0.25rem;
    }
    .gradient-subheader {
        font-size: 1.15rem;
        color: #475569;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Badges & Tags */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .badge-pool { background-color: #e0f2fe; color: #0369a1; }
    .badge-arena { background-color: #f0fdf4; color: #166534; }
    .badge-sector { background-color: #f1f5f9; color: #475569; }
    
    /* Style refinements for Streamlit tables */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    /* Adjust sidebar padding & styled divider */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# --- RECREATION FACILITIES DATA ---
# Pre-defined major Ottawa facilities covering West, East, South, and Central sectors
def get_facilities_data():
    json_path = "locations_data.json"
    if os.path.exists(json_path):
        try:
            import json
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if len(data) > 0:
                # Return all geocoded facilities from the JSON cache file
                return pd.DataFrame(data)
        except Exception:
            pass

    # Fallback to the 19 core facilities if JSON cache is not present
    data = [
        {
            "facility_name": "Richcraft Recreation Complex-Kanata",
            "address": "4101 Innovation Dr, Kanata, ON K2K 0J3",
            "sector": "West",
            "latitude": 45.3468,
            "longitude": -75.9221,
            "has_pool": True,
            "has_arena": False
        },
        {
            "facility_name": "Walter Baker Sports Centre",
            "address": "100 Malvern Dr, Nepean, ON K2J 2G9",
            "sector": "South",
            "latitude": 45.2755,
            "longitude": -75.7482,
            "has_pool": True,
            "has_arena": True
        },
        {
            "facility_name": "Goulbourn Recreation Complex",
            "address": "1500 Shea Rd, Stittsville, ON K2S 0B2",
            "sector": "West",
            "latitude": 45.2652,
            "longitude": -75.9238,
            "has_pool": True,
            "has_arena": True
        },
        {
            "facility_name": "Nepean Sportsplex",
            "address": "1701 Woodroffe Ave, Nepean, ON K2G 1W2",
            "sector": "South",
            "latitude": 45.3262,
            "longitude": -75.7329,
            "has_pool": True,
            "has_arena": True
        },
        {
            "facility_name": "Minto Recreation Complex-Barrhaven",
            "address": "3500 Cambrian Rd, Nepean, ON K2J 0V1",
            "sector": "South",
            "latitude": 45.2530,
            "longitude": -75.7766,
            "has_pool": True,
            "has_arena": True
        },
        {
            "facility_name": "François Dupuis Recreation Centre",
            "address": "2263 Portobello Blvd, Orléans, ON K4A 0X3",
            "sector": "East",
            "latitude": 45.4674,
            "longitude": -75.4623,
            "has_pool": True,
            "has_arena": False
        },
        {
            "facility_name": "St-Laurent Complex",
            "address": "525 Côté St, Ottawa, ON K1K 0Z8",
            "sector": "East",
            "latitude": 45.4243,
            "longitude": -75.6417,
            "has_pool": True,
            "has_arena": False
        },
        {
            "facility_name": "Ray Friel Recreation Complex",
            "address": "1585 Tenth Line Rd, Orléans, ON K1E 3E8",
            "sector": "East",
            "latitude": 45.4764,
            "longitude": -75.4770,
            "has_pool": True,
            "has_arena": True
        },
        {
            "facility_name": "Kanata Leisure Centre and Wave Pool",
            "address": "70 Aird Pl, Kanata, ON K2L 4B2",
            "sector": "West",
            "latitude": 45.3125,
            "longitude": -75.9080,
            "has_pool": True,
            "has_arena": False
        },
        {
            "facility_name": "Pinecrest Recreation Complex",
            "address": "2250 Torquay Ave, Ottawa, ON K2C 1J3",
            "sector": "West",
            "latitude": 45.3524,
            "longitude": -75.7915,
            "has_pool": True,
            "has_arena": True
        },
        {
            "facility_name": "Jack Purcell Community Centre",
            "address": "320 Elgin St, Ottawa, ON K2P 1M6",
            "sector": "Central",
            "latitude": 45.4158,
            "longitude": -75.6917,
            "has_pool": True,
            "has_arena": False
        },
        {
            "facility_name": "McNabb Recreation Centre",
            "address": "180 Percy St, Ottawa, ON K1R 6E5",
            "sector": "Central",
            "latitude": 45.4107,
            "longitude": -75.7029,
            "has_pool": False,
            "has_arena": True
        },
        {
            "facility_name": "Bob MacQuarrie Recreation Complex-Orléans",
            "address": "1490 Youville Dr, Orléans, ON K1C 2X8",
            "sector": "East",
            "latitude": 45.4622,
            "longitude": -75.5498,
            "has_pool": True,
            "has_arena": True
        },
        {
            "facility_name": "Brewer Pool and Arena",
            "address": "100 Brewer Way, Ottawa, ON K1S 5T1",
            "sector": "Central",
            "latitude": 45.3892,
            "longitude": -75.6967,
            "has_pool": True,
            "has_arena": True
        },
        {
            "facility_name": "Canterbury Recreation Complex",
            "address": "2185 Arch St, Ottawa, ON K1G 2H5",
            "sector": "Central",
            "latitude": 45.3814,
            "longitude": -75.6425,
            "has_pool": True,
            "has_arena": True
        },
        {
            "facility_name": "Shenkman Arts Centre",
            "address": "245 Centrum Blvd, Orléans, ON K1E 0A1",
            "sector": "East",
            "latitude": 45.48064,
            "longitude": -75.51129,
            "has_pool": False,
            "has_arena": False
        },
        {
            "facility_name": "Jim Durrell Recreation Centre",
            "address": "1265 Walkley Rd, Ottawa, ON K1V 6B9",
            "sector": "Central",
            "latitude": 45.37293,
            "longitude": -75.65978,
            "has_pool": False,
            "has_arena": True
        },
        {
            "facility_name": "Plant Recreation Centre",
            "address": "930 Somerset St W, Ottawa, ON K1R 6P8",
            "sector": "Central",
            "latitude": 45.40776,
            "longitude": -75.71460,
            "has_pool": True,
            "has_arena": False
        },
        {
            "facility_name": "Ron Kolbus Lakeside Centre",
            "address": "102 Greenview Dr, Ottawa, ON K2B 8J8",
            "sector": "West",
            "latitude": 45.36390,
            "longitude": -75.80144,
            "has_pool": False,
            "has_arena": False
        }
    ]
    return pd.DataFrame(data)


# --- GEOCODING LOGIC & CACHING ---
# Preset list of common regions inside Ottawa to guarantee an instant geocoding option
PRESET_LOCATIONS = {
    "Default: Ottawa City Hall (Central)": {"coords": (45.4214, -75.6909), "label": "Ottawa City Hall, 110 Laurier Ave W"},
    "West Sector: Richcraft Complex (Kanata)": {"coords": (45.3468, -75.9221), "label": "Richcraft Recreation Complex, Kanata"},
    "West Sector: Goulbourn (Stittsville)": {"coords": (45.2652, -75.9238), "label": "Goulbourn Recreation Complex, Stittsville"},
    "South Sector: Minto Complex (Barrhaven)": {"coords": (45.2530, -75.7766), "label": "Minto Recreation Complex, Barrhaven"},
    "South Sector: Walter Baker (Nepean)": {"coords": (45.2755, -75.7482), "label": "Walter Baker Sports Centre, Barrhaven/Nepean"},
    "East Sector: François Dupuis (Orléans)": {"coords": (45.4674, -75.4623), "label": "François Dupuis Recreation Centre, Orléans"},
    "Central Sector: Jack Purcell Centre (Downtown)": {"coords": (45.4158, -75.6917), "label": "Jack Purcell Community Centre, Elgin St"}
}

@st.cache_data(show_spinner=False)
def geocode_custom_address(address_str):
    """
    Attempts to geocode standard user inputs.
    Gracefully falls back to None if API errors out or fails to resolve.
    """
    if not address_str or len(address_str.strip()) < 3:
        return None
    try:
        # Standard free Nominatim geolocator (respect user_agent policies)
        geolocator = Nominatim(user_agent="ottawa_camp_spatial_discovery_planner_v1")
        
        # Append City context to make it easier for local search queries
        query = address_str
        query_lower = address_str.lower()
        if not any(x in query_lower for x in ["ottawa", "kanata", "orleans", "nepean", "stittsville", "barrhaven"]):
            query += ", Ottawa, ON"
            
        location = geolocator.geocode(query, timeout=4)
        if location:
            # Let's ensure the coordinate falls roughly in the Ottawa region bounds to prevent wild geocoding errors
            lat, lon = location.latitude, location.longitude
            if 44.8 <= lat <= 45.7 and -76.5 <= lon <= -75.0:
                return (lat, lon, location.address)
    except Exception:
        pass
    return None

# --- APP LAYOUT ---

# Top Banner Title
st.markdown('<div class="gradient-header">Ottawa Recreation Discovery Map</div>', unsafe_allow_html=True)
st.markdown('<div class="gradient-subheader">A visual pre-search tool for parents to filter facilities by proximity, amenities, and sectors before registering for Summer Camps.</div>', unsafe_allow_html=True)

# Main Facilities Dataframe
df_facilities = get_facilities_data()

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.markdown("### 📍 Location Configuration")

# Address Text Input
address_input = st.sidebar.text_input(
    "1. Home / Starting Address",
    value="",
    placeholder="e.g. 100 Laurier Ave W",
    help="Type in your home or work address to calculate real-world distances."
)

# Preset dropdown (Acts as direct fallback and easy testing controller)
preset_selection = st.sidebar.selectbox(
    "2. Preset Starting Location",
    options=list(PRESET_LOCATIONS.keys()),
    help="Use this dropdown to quickly mock your starting point or as an instant fallback if geocoding is slow."
)

# Resolve Home Coordinates
home_lat, home_lon = None, None
home_resolved_name = ""

# Determine coordinates based on input priority
if address_input.strip():
    with st.sidebar.spinner("Geocoding address..."):
        resolved = geocode_custom_address(address_input)
        if resolved:
            home_lat, home_lon, home_resolved_name = resolved
            st.sidebar.success(f"✓ Location resolved: {home_resolved_name[:40]}...")
        else:
            st.sidebar.warning("⚠️ Could not geocode address. Falling back to Preset Location.")

# If no text address is provided or geocoding failed, use selected preset
if home_lat is None or home_lon is None:
    preset_data = PRESET_LOCATIONS[preset_selection]
    home_lat, home_lon = preset_data["coords"]
    home_resolved_name = preset_data["label"]
    st.sidebar.info(f"📍 Active Origin: {preset_selection}")

# Add a spacer
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filter Criteria")

# 1. Sector Filters (West, East, South, Central)
sectors = sorted(df_facilities["sector"].unique())
selected_sectors = st.sidebar.multiselect(
    "Sectors",
    options=sectors,
    default=sectors,
    help="Select one or more sectors to display."
)

# 2. Amenities Toggles
st.sidebar.markdown("**Required Amenities**")
filter_pool = st.sidebar.checkbox("🏊 Has Swimming Pool", value=False)
filter_arena = st.sidebar.checkbox("⛸️ Has Arena", value=False)

# 3. Maximum Proximity Distance Slider
max_distance = st.sidebar.slider(
    "Maximum Proximity (km)",
    min_value=1,
    max_value=50,
    value=30,
    step=1,
    help="Limit facilities to those within this radius of your starting location."
)

# --- PROXIMITY CALCULATIONS ---
# Function to calculate distances dynamically (straight line / geodesic)
def calculate_distances(df, origin_lat, origin_lon):
    distances = []
    for idx, row in df.iterrows():
        dist = geodesic((origin_lat, origin_lon), (row["latitude"], row["longitude"])).kilometers
        distances.append(round(dist, 1))
    df = df.copy()
    df["distance_km"] = distances
    return df

# Function to fetch road distances and durations from OSRM in a single request
def compute_road_routing(origin_lat, origin_lon, df):
    # Cap destinations to keep it super fast and avoid OSRM query limit issues
    max_destinations = 40
    df_subset = df.head(max_destinations).copy()
    
    if df_subset.empty:
        return df_subset
        
    try:
        import urllib.request
        import json
        
        # OSRM expects longitude,latitude format
        origin_str = f"{origin_lon},{origin_lat}"
        dest_coords = [f"{row['longitude']},{row['latitude']}" for idx, row in df_subset.iterrows()]
        coords_str = ";".join([origin_str] + dest_coords)
        
        url = f"http://router.project-osrm.org/table/v1/driving/{coords_str}?sources=0&annotations=duration,distance"
        req = urllib.request.Request(url, headers={'User-Agent': 'ottawa_camp_registration_spatial_planner'})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            res = json.loads(response.read().decode())
            if res.get("code") == "Ok":
                road_dists_m = res["distances"][0][1:]  # skip source coordinate at index 0
                durations_s = res["durations"][0][1:]
                
                df_subset["road_distance_km"] = [round(d / 1000.0, 1) if d is not None else None for d in road_dists_m]
                df_subset["drive_time_mins"] = [int(round(t / 60.0)) if t is not None else None for t in durations_s]
                return df_subset
    except Exception:
        pass
        
    # Fallback to straight-line if API fails or offline
    df_subset["road_distance_km"] = df_subset["distance_km"]
    df_subset["drive_time_mins"] = None
    return df_subset

# Perform distance calculation
df_processed = calculate_distances(df_facilities, home_lat, home_lon)

# --- FILTER APPLICATION ---
# Filter by Sector
if selected_sectors:
    df_filtered = df_processed[df_processed["sector"].isin(selected_sectors)]
else:
    df_filtered = df_processed.copy()

# Filter by Amenities
if filter_pool:
    df_filtered = df_filtered[df_filtered["has_pool"] == True]
if filter_arena:
    df_filtered = df_filtered[df_filtered["has_arena"] == True]

# Filter by Radius Distance (straight-line filtering)
df_filtered = df_filtered[df_filtered["distance_km"] <= max_distance]

# Store the total number of facilities matching the filter criteria
total_matching_count = len(df_filtered)

# Sort by initial proximity before fetching road routes
df_filtered = df_filtered.sort_values(by="distance_km", ascending=True).reset_index(drop=True)

# Fetch road distances & driving durations for the closest matching facilities
df_filtered = compute_road_routing(home_lat, home_lon, df_filtered)

# Sort by Road Proximity
if "road_distance_km" in df_filtered.columns and not df_filtered.empty:
    # Handle cases where some might be None (API fallback)
    df_filtered = df_filtered.sort_values(by="road_distance_km", ascending=True).reset_index(drop=True)

# --- KPI METRIC CARDS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Facilities Found</div>
        <div class="metric-value">{total_matching_count} <span style="font-size:1.1rem; font-weight:normal; color:#64748b;">/ {len(df_facilities)} total</span></div>
        <div class="metric-subtitle">Within {max_distance} km radius</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if not df_filtered.empty:
        closest = df_filtered.iloc[0]
        road_dist = closest.get('road_distance_km')
        drive_time = closest.get('drive_time_mins')
        
        if drive_time is not None:
            metric_subtitle = f"🚗 {drive_time} mins drive ({road_dist} km by road)"
        else:
            metric_subtitle = f"Only {closest['distance_km']} km away (straight-line)"
            
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🥇 Closest (Road Dist)</div>
            <div class="metric-value" style="font-size:1.4rem; padding-top:4px;">{closest['facility_name']}</div>
            <div class="metric-subtitle">{metric_subtitle}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🥇 Closest Facility</div>
            <div class="metric-value">—</div>
            <div class="metric-subtitle">No matching facilities in range</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📍 Your Start Origin</div>
        <div class="metric-value" style="font-size:1.35rem; padding-top:4px;">{home_resolved_name.split(',')[0]}</div>
        <div class="metric-subtitle">Coords: {home_lat:.4f}, {home_lon:.4f}</div>
    </div>
    """, unsafe_allow_html=True)


# --- LAYOUT - MAP (TOP) & TABLE (BOTTOM) ---
st.markdown("### 🗺️ Facility Spatial Planner")

# Creating folium map centered on current origin
map_center = [home_lat, home_lon]
# Initialize map with standard Cartodb Positron tile (modern, elegant, high contrast light map)
m = folium.Map(location=map_center, zoom_start=11, tiles="cartodbpositron")

# Plot Home Location
home_tooltip = f"<b>Your Start Location</b><br>{home_resolved_name}"
folium.Marker(
    location=[home_lat, home_lon],
    popup=folium.Popup(home_tooltip, max_width=300),
    tooltip="Active Origin",
    icon=folium.Icon(color="red", icon="star", prefix="fa")
).add_to(m)

# Add radius buffer circle around home to help visualize distance
folium.Circle(
    location=[home_lat, home_lon],
    radius=max_distance * 1000, # convert km to meters
    color="#0d9488",
    fill=True,
    fill_color="#0d9488",
    fill_opacity=0.08,
    weight=1.5,
    dash_array="5, 5",
    tooltip=f"{max_distance} km Search Radius"
).add_to(m)

# Plot matching facilities as markers
for idx, row in df_filtered.iterrows():
    # Build styled popup HTML for the facility
    amenities_html = ""
    if row["has_pool"]:
        amenities_html += '<span class="badge badge-pool">🏊 Pool</span>'
    if row["has_arena"]:
        amenities_html += '<span class="badge badge-arena">⛸️ Arena</span>'
        
    road_info_html = ""
    if "drive_time_mins" in row and row["drive_time_mins"] is not None:
        road_info_html = f"""
            <b>Commute (Road):</b> {row['road_distance_km']} km ({row['drive_time_mins']} mins drive)<br>
            <b>Straight-line:</b> {row['distance_km']} km
        """
    else:
        road_info_html = f"<b>Distance to Home:</b> {row['distance_km']} km"
        
    popup_content = f"""
    <div style="font-family:'Outfit', sans-serif; min-width: 220px;">
        <h4 style="margin:0 0 5px 0; color:#0f172a; font-weight:600;">{row['facility_name']}</h4>
        <span class="badge badge-sector">{row['sector']} Sector</span><br>
        <p style="margin:8px 0; font-size:12px; color:#475569;">
            <b>Address:</b> {row['address']}<br>
            {road_info_html}
        </p>
        <div style="margin-bottom: 12px;">{amenities_html}</div>
        <hr style="border:0; border-top:1px solid #e2e8f0; margin:8px 0;">
        <a href="https://ottawa.ca/en/recreation-and-parks/facilities/recreation-complexes-and-community-centres" 
           target="_blank" 
           style="background-color:#0d9488; color:white; padding:6px 12px; text-decoration:none; border-radius:6px; font-size:11px; font-weight:bold; display:inline-block;">
           Ottawa Registration Portal ↗
        </a>
    </div>
    """
    
    # Custom colored pins based on sector
    marker_color = "cadetblue"
    if row["sector"] == "West":
        marker_color = "blue"
    elif row["sector"] == "East":
        marker_color = "orange"
    elif row["sector"] == "South":
        marker_color = "purple"
    elif row["sector"] == "Central":
        marker_color = "darkgreen"
        
    icon_type = "info-sign"
    if row["has_pool"] and row["has_arena"]:
        icon_type = "map-marker"
        
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=folium.Popup(popup_content, max_width=280),
        tooltip=f"{row['facility_name']} ({row['distance_km']} km)",
        icon=folium.Icon(color=marker_color, icon=icon_type)
    ).add_to(m)

# Render Folium Map in Streamlit
map_data = st_folium(m, height=450, width="100%", returned_objects=[])

# --- PROXIMITY TABLE ---
if total_matching_count > 40:
    st.markdown("### 📋 Proximity Facility Summary (Showing top 40 closest by road)")
else:
    st.markdown("### 📋 Proximity Facility Summary")
if not df_filtered.empty:
    # Format table for cleaner rendering
    display_df = df_filtered.copy()
    display_df["Pool"] = display_df["has_pool"].apply(lambda x: "🏊 Yes" if x else "❌ No")
    display_df["Arena"] = display_df["has_arena"].apply(lambda x: "⛸️ Yes" if x else "❌ No")
    
    # Check if road distance columns are present
    has_road = "road_distance_km" in display_df.columns
    if has_road:
        display_df["Drive Time"] = display_df["drive_time_mins"].apply(lambda x: f"🚗 {x} mins" if x is not None else "N/A")
        display_df["Road Distance"] = display_df["road_distance_km"].apply(lambda x: f"🛣️ {x} km" if x is not None else "N/A")
        
    # Rename columns for presentation
    display_df = display_df.rename(columns={
        "facility_name": "Facility Name",
        "sector": "Sector",
        "distance_km": "Straight-line (km)",
        "address": "Address"
    })
    
    # Select specific columns to show
    if has_road:
        show_cols = ["Facility Name", "Sector", "Drive Time", "Road Distance", "Straight-line (km)", "Pool", "Arena", "Address"]
    else:
        show_cols = ["Facility Name", "Sector", "Straight-line (km)", "Pool", "Arena", "Address"]
    
    # Styled Streamlit DataFrame
    st.dataframe(
        display_df[show_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Straight-line (km)": st.column_config.NumberColumn(
                format="%.1f km"
            )
        }
    )
else:
    st.warning("No facilities match your active search filters. Adjust filters in the sidebar to view more facilities.")
