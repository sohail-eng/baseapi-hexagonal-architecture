"""
SQLAlchemy mapping for City entity.
"""

from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from sqlalchemy.orm import mapped_column

from app.domain.entities.city import City
from app.domain.value_objects.city_id import CityId
from app.domain.value_objects.city_name import CityName
from app.domain.value_objects.state_id import StateId
from app.domain.value_objects.state_code import StateCode
from app.domain.value_objects.state_name import StateName
from app.domain.value_objects.country_id import CountryId
from app.domain.value_objects.country_code import CountryCode
from app.domain.value_objects.country_name import CountryName
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.wiki_data_id import WikiDataId
from app.infrastructure.persistence_sqla.registry import mapping_registry


def map_cities_table() -> None:
    """Map City entity to database table."""
    
    @mapping_registry.mapped
    class CitiesTable:
        __tablename__ = "cities"
        
        # Primary key
        id = mapped_column(Integer, primary_key=True, index=True)
        
        # City information
        city_id = mapped_column(Integer, index=True)
        name = mapped_column(String(100), nullable=False, index=True)
        state_id = mapped_column(Integer, nullable=False, index=True)
        state_code = mapped_column(String(10), nullable=True, index=True)
        state_name = mapped_column(String(100), nullable=False)
        country_id = mapped_column(Integer, nullable=False, index=True)
        country_code = mapped_column(String(2), nullable=False, index=True)
        country_name = mapped_column(String(100), nullable=False)
        latitude = mapped_column(Float, nullable=True)
        longitude = mapped_column(Float, nullable=True)
        wikiDataId = mapped_column(String(50), nullable=True, index=True)
        
        # Add constraints for coordinates
        __table_args__ = (
            CheckConstraint('latitude >= -90 AND latitude <= 90', name='check_city_latitude_range'),
            CheckConstraint('longitude >= -180 AND longitude <= 180', name='check_city_longitude_range'),
        )
    
    # Register the mapping
    mapping_registry.map_imperatively(
        City,
        CitiesTable,
        properties={
            "id": mapping_registry.column_property(
                CitiesTable.id,
                CityId
            ),
            "name": mapping_registry.column_property(
                CitiesTable.name,
                CityName
            ),
            "state_id": mapping_registry.column_property(
                CitiesTable.state_id,
                StateId
            ),
            "state_code": mapping_registry.column_property(
                CitiesTable.state_code,
                StateCode
            ),
            "state_name": mapping_registry.column_property(
                CitiesTable.state_name,
                StateName
            ),
            "country_id": mapping_registry.column_property(
                CitiesTable.country_id,
                CountryId
            ),
            "country_code": mapping_registry.column_property(
                CitiesTable.country_code,
                CountryCode
            ),
            "country_name": mapping_registry.column_property(
                CitiesTable.country_name,
                CountryName
            ),
            "coordinates": mapping_registry.column_property(
                CitiesTable.latitude,
                CitiesTable.longitude,
                Coordinates
            ),
            "wiki_data_id": mapping_registry.column_property(
                CitiesTable.wikiDataId,
                WikiDataId
            ),
        }
    )
