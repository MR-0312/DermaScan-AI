"""
=================================================================
HOSPITAL FINDER — India-Specific
=================================================================
"""

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
    "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
    "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
    "West Bengal", "Delhi", "Chandigarh", "Puducherry",
    "Jammu and Kashmir", "Ladakh",
]


class HospitalFinder:
    """
    Find nearby hospitals in India using Google Maps URL.
    No API key needed — generates search URLs.
    """
    
    def __init__(self):
        self.country = "India"
    
    def search(self, query: str, city: str, state: str) -> dict:
        """
        Generate Google Maps search for hospitals in a specific city.
        
        Args:
            query: Search type (e.g., "skin cancer specialist")
            city: City name
            state: State name
        
        Returns:
            Dictionary with maps_url and search info
        """
        location = f"{city}, {state}, India"
        full_query = f"{query} in {location}"
        encoded = full_query.replace(" ", "+")
        
        maps_url = f"https://www.google.com/maps/search/{encoded}"
        embed_url = f"https://maps.google.com/maps?q={encoded}&z=13&output=embed"
        
        return {
            "maps_url": maps_url,
            "embed_url": embed_url,
            "query": full_query,
            "city": city,
            "state": state,
            "location": location,
        }
    
    def get_emergency_numbers(self) -> dict:
        """Indian emergency numbers."""
        return {
            "Emergency": "112",
            "Ambulance": "108",
            "Health Helpline": "104",
            "AIIMS Delhi": "011-26588500",
            "National Cancer Helpline": "1800-11-6006",
        }