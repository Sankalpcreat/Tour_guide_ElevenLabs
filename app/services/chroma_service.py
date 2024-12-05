import chromadb
import logging
from typing import Dict, List, Optional, Union
from math import radians, sin, cos, sqrt, atan2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChromaService:
    def __init__(self, db_path: str):
        try:
            self.client = chromadb.Client(chromadb.config.Settings(persist_directory=db_path))
            self.collection = self.client.get_or_create_collection(name="historical_locations", metadata={"description": "Historical locations and landmarks database"})
            logger.info("ChromaDB connection established successfully")
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            raise

    def store_location(self, location_data: Dict[str, Union[str, float]]) -> bool:
        try:
            metadata = {
                "name": location_data["name"],
                "latitude": float(location_data["latitude"]),
                "longitude": float(location_data["longitude"]),
                "image": location_data.get("image", "")
            }
            self.collection.add(ids=[location_data["id"]], embeddings=[location_data["embedding"]], metadatas=[metadata])
            logger.info(f"Location stored successfully: {location_data['name']}")
            return True
        except Exception as e:
            logger.error(f"Error storing location {location_data.get('name', '')}: {e}")
            return False

    def get_location(self, location_id: str) -> Optional[Dict]:
        try:
            result = self.collection.get(ids=[location_id], include=['embeddings', 'metadatas'])
            if result and 'embeddings' in result and 'metadatas' in result:
                vector = result['embeddings'][0].flatten().tolist()
                metadata = result['metadatas'][0]
                return {
                    'id': location_id,
                    'name': metadata.get('name'),
                    'latitude': metadata.get('latitude'),
                    'longitude': metadata.get('longitude'),
                    'image': metadata.get('image'),
                    'embedding': vector
                }
            return None
        except Exception as e:
            logger.error(f"Error retrieving location {location_id}: {e}")
            return None

    def search_similar_locations(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        try:
            collection_size = self.collection.count()
            adjusted_top_k = min(top_k, collection_size)
            results = self.collection.query(query_embeddings=[query_embedding], n_results=adjusted_top_k, include=['embeddings', 'metadatas', 'distances'])
            locations = []
            if results and 'embeddings' in results:
                for i, (embedding, metadata, distance) in enumerate(zip(results['embeddings'][0], results['metadatas'][0], results['distances'][0])):
                    locations.append({
                        'id': results['ids'][0][i],
                        'name': metadata.get('name'),
                        'latitude': metadata.get('latitude'),
                        'longitude': metadata.get('longitude'),
                        'image': metadata.get('image'),
                        'similarity_score': 1.0 - distance
                    })
            return locations
        except Exception as e:
            logger.error(f"Error searching similar locations: {e}")
            return []

    def get_locations_in_radius(self, lat: float, lon: float, radius_km: float) -> List[Dict]:
        try:
            all_locations = self.collection.get(include=['metadatas'])
            if not all_locations or 'metadatas' not in all_locations:
                return []
            
            def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
                R = 6371
                lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
                dlat, dlon = lat2 - lat1, lon2 - lon1
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * atan2(sqrt(a), sqrt(1-a))
                return R * c
            
            nearby_locations = []
            for i, metadata in enumerate(all_locations['metadatas']):
                try:
                    location_lat, location_lon = float(metadata['latitude']), float(metadata['longitude'])
                    distance = haversine_distance(lat, lon, location_lat, location_lon)
                    if distance <= radius_km:
                        nearby_locations.append({
                            'id': all_locations['ids'][i],
                            'name': metadata.get('name'),
                            'latitude': location_lat,
                            'longitude': location_lon,
                            'image': metadata.get('image'),
                            'distance_km': round(distance, 2)
                        })
                except (ValueError, KeyError):
                    continue
            return sorted(nearby_locations, key=lambda x: x['distance_km'])
        except Exception as e:
            logger.error(f"Error finding locations in radius: {e}")
            return []

