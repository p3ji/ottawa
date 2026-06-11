import json
import time
import os
from geopy.geocoders import Nominatim

# List of all 174 locations provided by the user
locations_list = [
    "Albion-Heatherington Recreation Centre",
    "Alexander Community Centre",
    "Alfred Taylor Recreation Centre",
    "Alta Vista Public School",
    "Aquaview Community Hall",
    "Arch Street Public School",
    "Atrium Park",
    "Avalon Public School",
    "Bayshore Community Building",
    "Beacon Hill North Community Hall",
    "Bearbrook Community Centre",
    "Bearbrook Pool",
    "Beaverbrook Pool - Kanata",
    "Bell Centennial Arena",
    "Bell High School",
    "Ben Franklin Place",
    "Billings Estate National Historic Site",
    "Bingham Park",
    "Blackburn Hamlet Community Hall",
    "Bob MacQuarrie Recreation Complex - Orléans",
    "Bob Monette Community Center",
    "Brewer Arena",
    "Brewer Pool",
    "Briargreen Public School",
    "Bridlewood Community Elementary School",
    "Britannia Park",
    "Canterbury Recreation Complex",
    "CardelRec Complex (Goulbourn)",
    "Carleton Heights Community Centre",
    "Carleton Heights Park",
    "Carleton Heights Public School",
    "Carlington Recreation Centre",
    "Carp Memorial Hall",
    "Cavanagh Community Centre",
    "Centennial Park",
    "Champagne Fitness Centre",
    "Chapman Mills Community Building",
    "Charlie Conacher Community Building",
    "Churchill Seniors’ Recreation Centre",
    "Collège catholique Franco-Ouest",
    "Constance Bay Community Centre",
    "Corkery Community Centre",
    "Corkstown Pool",
    "Craig Henry Community Building",
    "Crestview Pool",
    "Cumberland Heritage Village Museum",
    "Deborah Anne Kirwan Pool",
    "Dempsey Community Centre",
    "Diane Deans Greenboro Community Centre",
    "Dogwood Park (Munster)",
    "Earl Armstrong Arena",
    "Entrance Pool",
    "Eva James Memorial Community Centre",
    "Fairfields Heritage House",
    "Fallingbrook Community Elementary School",
    "Fisher Park Community Centre",
    "Fitzroy Harbour Community Centre",
    "Foster Farm Community Centre",
    "Four Seasons Park",
    "François Dupuis Recreation Centre",
    "Fred G. Barrett Arena",
    "Frederick Banting Secondary Alternate Program",
    "Fringewood Community Centre",
    "Fringewood Park",
    "General Burns Pool",
    "Genest Pool",
    "Glebe Community Centre",
    "Glen Cairn Community Centre",
    "Greely Community Centre",
    "Greely Elementary School",
    "Heron Park",
    "Heron Road Community Centre",
    "Hillcrest High School",
    "Hintonburg Community Centre",
    "Hunt Club-Riverside Park Community Centre",
    "Huntley Centennial Public School",
    "Huntley Community Centre",
    "Huntley Mess Hall",
    "J. A. Dulude Arena",
    "Jack Charron Arena",
    "Jack Purcell Community Centre",
    "Jim Durrell Recreation Centre",
    "Jockvale Elementary School",
    "John G. Mlacak Centre/Kanata Seniors' Centre",
    "Johnny Leroux Stittsville Community Arena",
    "Jules Morin Park",
    "Kanata Highlands Public School",
    "Kanata Leisure Centre and Wave Pool",
    "Katimavik Outdoor Pool",
    "Katimavik Public School",
    "Ken Ross Park",
    "Kinburn Community Centre",
    "Klondike Road Park",
    "Lansdowne Park",
    "Lois Kemp Arena",
    "Longfields-Davidson Heights Secondary School",
    "Lowertown Community Centre and Pool",
    "Lynwood Community Building",
    "Maki House Community Bldng.",
    "Manordale Public School",
    "Manotick Community Centre",
    "Manotick Public School",
    "Maplewood Secondary School",
    "Margaret Rywak Community Building",
    "McCarthy Park",
    "McKellar Park",
    "McNabb Recreation Centre",
    "Meadowlands Public School",
    "Metcalfe Community Centre",
    "Michele Heights Community Centre",
    "Mino Mikan Elementary School",
    "Minto Recreation Complex-Barrhaven",
    "Mooney's Bay Park",
    "Munster Community Center",
    "Munster Elementary School",
    "Navan Memorial Community Centre",
    "Nepean Creative Arts Centre",
    "Nepean Museum",
    "Nepean Seniors Center",
    "Nepean Sportsplex",
    "Nepean Visual Arts Centre",
    "Notre Dame Des Champs Community Hall",
    "Old Town Hall (Kanata)",
    "Osgoode Community Centre",
    "Osgoode Township High School",
    "Overbrook Community Centre",
    "Overbrook Park",
    "Owl Park",
    "Pat Clark Community Centre",
    "Pinecrest Park",
    "Pinecrest Public School",
    "Pinecrest Recreation Complex",
    "Pinhey's Point Historic Site",
    "Plant Recreation Centre",
    "Public Education Training Centre",
    "Queen Elizabeth Public School",
    "R.J. Kennedy Arena and Community Hall",
    "Ray Friel Recreation Complex",
    "Richcraft Recreation Complex-Kanata",
    "Richelieu-Vanier Community Centre",
    "Richmond Lions Community Park",
    "Richmond Memorial Community Centre",
    "Richmond Public School",
    "Rideauview Community Centre",
    "Ridgemont High School",
    "Roberta Bondar Public School",
    "Rockcliffe Park Community Centre",
    "Ron Kolbus Lakeside Centre",
    "Routhier Community Centre",
    "S.S.#1 Community Centre",
    "Sandy Hill Arena",
    "Sandy Hill Community Centre",
    "Sawmill Creek Pool and Community Centre",
    "Shenkman Arts Centre",
    "Sir Robert Borden High School",
    "Sir Wilfrid Laurier Secondary School",
    "South Carleton High School",
    "South Fallingbrook Community Centre",
    "Southpointe Community Building",
    "Splash Wave Pool",
    "St-Laurent Complex",
    "St. Emily School",
    "St. Germain Park (Sandy Hill Community Centre)",
    "St. Juan Diego School",
    "St. Michael School, Fitzroy",
    "Stonecrest Elementary School",
    "Stuemer Park/Petrie Island",
    "Tanglewood Community Building",
    "Terry Fox Athletic Facility",
    "Tom Brown Arena",
    "Tony Graham Community Park",
    "Tony Graham Recreation Complex-Kanata",
    "Trend Arlington Community Building",
    "Trillium Elementary School",
    "Vernon Recreation Centre",
    "Vimy Ridge Public School",
    "Vincent Massey Public School",
    "W. Erskine Johnston Arena",
    "W.O. Mitchell Elementary School",
    "Walter Baker Sports Centre",
    "West Carleton Community Complex",
    "Westcliffe Community Building",
    "École secondaire catholique Pierre-Savard",
    "École élémentaire publique Francojeunesse"
]

CUSTOM_SEARCH_QUERIES = {
    "CardelRec Complex (Goulbourn)": "1500 Shea Rd, Stittsville, ON",
    "Deborah Anne Kirwan Pool": "Deborah Kirwan Pool, 2930 Heatherington Rd, Ottawa, ON",
    "Maki House Community Bldng.": "19 Bayne Ave, Ottawa, ON",
    "Tony Graham Recreation Complex-Kanata": "100 Charlie Rogers Place, Kanata, ON",
    "Tony Graham Community Park": "100 Charlie Rogers Place, Kanata, ON",
    "Beaverbrook Pool - Kanata": "Beaverbrook Outdoor Pool, Kanata, ON",
    "Bob MacQuarrie Recreation Complex - Orléans": "Bob MacQuarrie Recreation Complex, Orleans, ON",
    "St. Germain Park (Sandy Hill Community Centre)": "Sandy Hill Community Centre, Ottawa, ON",
    "St. Michael School, Fitzroy": "St. Michael's School, Fitzroy Harbour, ON",
    "Stuemer Park/Petrie Island": "Petrie Island Park, Ottawa, ON",
    "Public Education Training Centre": "Ottawa, ON",
    "Diane Deans Greenboro Community Centre": "Greenboro Community Centre, Ottawa, ON",
    "Johnny Leroux Stittsville Community Arena": "Johnny Leroux Arena, Stittsville, ON",
    "John G. Mlacak Centre/Kanata Seniors' Centre": "John G. Mlacak Centre, Kanata, ON",
    "W. Erskine Johnston Arena": "Erskine Johnston Arena, Carp, ON",
    "R.J. Kennedy Arena and Community Hall": "1115 Dunning Rd, Cumberland, ON",
    "Eva James Memorial Community Centre": "Amherst Crescent, Ottawa, ON",
    "François Dupuis Recreation Centre": "François Dupuis Recreation Centre, Orleans, ON",
    "Bob Monette Community Center": "2295 Tenth Line Rd, Orleans, ON",
    "Minto Recreation Complex-Barrhaven": "Minto Recreation Complex, Barrhaven, ON",
    "Albion-Heatherington Recreation Centre": "1560 Heatherington Rd, Ottawa, ON",
    "Aquaview Community Hall": "Aquaview Dr, Ottawa, ON",
    "Beacon Hill North Community Hall": "Beacon Hill North, Ottawa, ON",
    "Billings Estate National Historic Site": "2100 Cabot St, Ottawa, ON",
    "Blackburn Hamlet Community Hall": "Glen Park Dr, Ottawa, ON",
    "Champagne Fitness Centre": "321 King Edward Ave, Ottawa, ON",
    "Chapman Mills Community Building": "424 Chapman Mills Dr, Nepean, ON",
    "Charlie Conacher Community Building": "Arena Rd, Ottawa, ON",
    "Craig Henry Community Building": "130 Craig Henry Dr, Nepean, ON",
    "Fairfields Heritage House": "3082 Richmond Rd, Ottawa, ON",
    "Fitzroy Harbour Community Centre": "Fitzroy Harbour, ON",
    "Frederick Banting Secondary Alternate Program": "1453 Stittsville Main St, Stittsville, ON",
    "Hunt Club-Riverside Park Community Centre": "3320 Paul Anka Dr, Ottawa, ON",
    "Katimavik Public School": "64 Chimo Dr, Kanata, ON",
    "Lois Kemp Arena": "Blackburn Arena, Ottawa, ON",
    "Lowertown Community Centre and Pool": "40 Cobourg St, Ottawa, ON",
    "Margaret Rywak Community Building": "Knoxdale Community Centre, Ottawa",
    "Navan Memorial Community Centre": "1295 Colonial Rd, Navan, ON",
    "Nepean Seniors Center": "1701 Woodroffe Ave, Nepean, ON",
    "Nepean Visual Arts Centre": "1701 Woodroffe Ave, Nepean, ON",
    "Notre Dame Des Champs Community Hall": "3659 Navan Rd, Orleans, ON",
    "Pinhey's Point Historic Site": "Pinhey Point, Ottawa, ON",
    "Richmond Memorial Community Centre": "6095 Perth St, Richmond, ON",
    "Rockcliffe Park Community Centre": "380 Springfield Rd, Ottawa, ON",
    "Terry Fox Athletic Facility": "2960 Riverside Dr, Ottawa, ON"
}

def clean_name_for_query(name):
    # If there is a custom query mapped, return it
    if name in CUSTOM_SEARCH_QUERIES:
        return CUSTOM_SEARCH_QUERIES[name]
    
    # Strip some suffixes or formatting for cleaner lookup
    clean = name
    if "Community Bldng." in clean:
        clean = clean.replace("Community Bldng.", "Community Centre")
    if "Community Building" in clean:
        clean = clean.replace("Community Building", "Community Centre")
    
    # Ensure it targets Ottawa, ON
    if "ottawa" not in clean.lower() and "kanata" not in clean.lower() and "orleans" not in clean.lower() and "stittsville" not in clean.lower() and "barrhaven" not in clean.lower() and "nepean" not in clean.lower():
        clean += ", Ottawa, ON"
    return clean

def get_sector_from_coords(lat, lon):
    # Sector geographic classification boundaries
    if lon < -75.80:
        return "West"
    elif lon > -75.63:
        return "East"
    elif lat < 45.37:
        return "South"
    else:
        return "Central"

def has_pool_check(name):
    # Pool keyword detection
    name_l = name.lower()
    pool_keywords = ["pool", "complex", "sportsplex", "aquaview", "fitness", "st-laurent"]
    return any(k in name_l for k in pool_keywords)

def has_arena_check(name):
    # Strict list of valid arena facilities based on official City of Ottawa and ottawapublicskating.ca lists
    arena_facilities = {
        "Bell Centennial Arena",
        "Bob MacQuarrie Recreation Complex - Orléans",
        "Brewer Arena",
        "Canterbury Recreation Complex",
        "CardelRec Complex (Goulbourn)",
        "Earl Armstrong Arena",
        "Fred G. Barrett Arena",
        "Jack Charron Arena",
        "Jim Durrell Recreation Centre",
        "John G. Mlacak Centre/Kanata Seniors' Centre",
        "Johnny Leroux Stittsville Community Arena",
        "Lansdowne Park",
        "Lois Kemp Arena",
        "Manotick Community Centre",
        "McNabb Recreation Centre",
        "Metcalfe Community Centre",
        "Minto Recreation Complex-Barrhaven",
        "Navan Memorial Community Centre",
        "Nepean Sportsplex",
        "Osgoode Community Centre",
        "Pinecrest Recreation Complex",
        "R.J. Kennedy Arena and Community Hall",
        "Ray Friel Recreation Complex",
        "Richmond Memorial Community Centre",
        "Sandy Hill Arena",
        "St-Laurent Complex",
        "Tom Brown Arena",
        "Tony Graham Recreation Complex-Kanata",
        "W. Erskine Johnston Arena",
        "Walter Baker Sports Centre"
    }
    return name in arena_facilities

def main():
    json_path = "locations_data.json"
    
    # Load existing cached locations if they exist to avoid duplicate API requests
    cached_data = {}
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                cached_list = json.load(f)
                cached_data = {item["facility_name"]: item for item in cached_list}
                print(f"Loaded {len(cached_data)} cached facilities from {json_path}")
        except Exception as e:
            print(f"Error reading {json_path}: {e}")
            
    geolocator = Nominatim(user_agent="ottawa_rec_caching_geocoder_v2")
    results = []
    
    print("Starting geocoding process...")
    for idx, name in enumerate(locations_list):
        if name in cached_data:
            # Re-geocode if the cached entry was a fallback to City Hall
            if "fallback" not in cached_data[name]["address"].lower():
                cached_item = cached_data[name]
                cached_item["has_pool"] = has_pool_check(name)
                cached_item["has_arena"] = has_arena_check(name)
                results.append(cached_item)
                continue
            
        query = clean_name_for_query(name)
        print(f"[{idx+1}/{len(locations_list)}] Geocoding: '{name}' (Query: '{query}')")
        
        lat, lon, address = None, None, ""
        
        try:
            location = geolocator.geocode(query, timeout=6)
            if location:
                # Bounding box filter for Ottawa region
                if 44.7 <= location.latitude <= 45.8 and -76.6 <= location.longitude <= -74.8:
                    lat = location.latitude
                    lon = location.longitude
                    address = location.address
            
            # If standard geocoding failed, try a broader search using name only
            if lat is None:
                short_query = name.split(' - ')[0].split('(')[0] + ", Ottawa, ON"
                location = geolocator.geocode(short_query, timeout=6)
                if location:
                    if 44.7 <= location.latitude <= 45.8 and -76.6 <= location.longitude <= -74.8:
                        lat = location.latitude
                        lon = location.longitude
                        address = location.address
                        print(f"  -> Resolved via fallback short query: '{short_query}'")
                        
            # If all failed, write a fallback (Ottawa City Hall)
            if lat is None:
                print(f"  -> WARNING: Failed to geocode '{name}'. Using Ottawa City Hall fallback.")
                lat, lon = 45.4214, -75.6909
                address = f"{name} (Location coords fallback to Ottawa City Hall), Ottawa, ON"
                
        except Exception as e:
            print(f"  -> Error geocoding '{name}': {e}. Using City Hall fallback.")
            lat, lon = 45.4214, -75.6909
            address = f"{name} (Geocode error fallback to Ottawa City Hall), Ottawa, ON"
            
        sector = get_sector_from_coords(lat, lon)
        pool = has_pool_check(name)
        arena = has_arena_check(name)
        
        # Format the resolved address for clean display (strip long postal/country details)
        clean_address = address
        if address:
            addr_parts = address.split(',')
            # Take first few parts to keep it readable
            clean_address = ", ".join([p.strip() for p in addr_parts[:3]])
            
        item = {
            "facility_name": name,
            "address": clean_address,
            "latitude": lat,
            "longitude": lon,
            "sector": sector,
            "has_pool": pool,
            "has_arena": arena
        }
        
        results.append(item)
        cached_data[name] = item
        
        # Save cache immediately to prevent losing progress
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(list(cached_data.values()), f, indent=4, ensure_ascii=False)
            
        # Respect Nominatim API usage policy limits (minimum 1 second between requests)
        time.sleep(1.2)
        
    # Save cache outside the loop to write all updates (including cache-hit updates) to disk
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(list(cached_data.values()), f, indent=4, ensure_ascii=False)
        
    print(f"Finished geocoding! Saved {len(results)} locations to {json_path}")

if __name__ == "__main__":
    main()
