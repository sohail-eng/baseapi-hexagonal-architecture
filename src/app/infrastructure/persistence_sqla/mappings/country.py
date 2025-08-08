"""
SQLAlchemy mapping for Country entity.
"""

from sqlalchemy import Column, Integer, String, Float, JSON, CheckConstraint
from sqlalchemy.orm import mapped_column

from app.domain.entities.country import Country
from app.domain.value_objects.country_id import CountryId
from app.domain.value_objects.country_name import CountryName
from app.domain.value_objects.iso_code import IsoCode
from app.domain.value_objects.coordinates import Coordinates
from app.infrastructure.persistence_sqla.registry import mapping_registry


def map_countries_table() -> None:
    """Map Country entity to database table."""
    
    @mapping_registry.mapped
    class CountriesTable:
        __tablename__ = "countries"
        
        # Primary key
        id = mapped_column(Integer, primary_key=True, index=True)
        
        # Country information
        country_id = mapped_column(Integer, index=True)
        name = mapped_column(String(100), nullable=False, index=True)
        iso3 = mapped_column(String(3), unique=True, nullable=False, index=True)
        iso2 = mapped_column(String(2), nullable=True, index=True)
        numeric_code = mapped_column(String(3), nullable=True)
        phonecode = mapped_column(String(20), nullable=True)
        capital = mapped_column(String(100), nullable=True)
        currency = mapped_column(String(3), nullable=True)
        currency_name = mapped_column(String(50), nullable=True)
        currency_symbol = mapped_column(String(10), nullable=True)
        tld = mapped_column(String(10), nullable=True)
        native = mapped_column(String(100), nullable=True)
        nationality = mapped_column(String(100), nullable=True)
        timezones = mapped_column(JSON, nullable=True)  # Store as JSON array
        latitude = mapped_column(Float, nullable=True)
        longitude = mapped_column(Float, nullable=True)
        emoji = mapped_column(String(10), nullable=True)
        emojiU = mapped_column(String(20), nullable=True)
        region = mapped_column(String(50), nullable=True, index=True)
        subregion = mapped_column(String(50), nullable=True, index=True)
        
        # Add constraints for coordinates
        __table_args__ = (
            CheckConstraint('latitude >= -90 AND latitude <= 90', name='check_latitude_range'),
            CheckConstraint('longitude >= -180 AND longitude <= 180', name='check_longitude_range'),
        )
    
    # Register the mapping
    mapping_registry.map_imperatively(
        Country,
        CountriesTable,
        properties={
            "id": mapping_registry.column_property(
                CountriesTable.id,
                CountryId
            ),
            "name": mapping_registry.column_property(
                CountriesTable.name,
                CountryName
            ),
            "iso3": mapping_registry.column_property(
                CountriesTable.iso3,
                IsoCode
            ),
            "iso2": mapping_registry.column_property(
                CountriesTable.iso2,
                IsoCode
            ),
            "coordinates": mapping_registry.column_property(
                CountriesTable.latitude,
                CountriesTable.longitude,
                Coordinates
            ),
        }
    )
