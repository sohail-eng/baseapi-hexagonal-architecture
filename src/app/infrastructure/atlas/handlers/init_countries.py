import csv
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

from sqlalchemy import Select, and_, select
from sqlalchemy.exc import SQLAlchemyError

from app.infrastructure.adapters.types import MainAsyncSession
from app.infrastructure.exceptions.gateway import DataMapperError
from app.infrastructure.adapters.constants import DB_QUERY_FAILED
from app.infrastructure.persistence_sqla.mappings.country import map_countries_table
from app.infrastructure.persistence_sqla.registry import mapping_registry

log = logging.getLogger(__name__)


class InitCountriesResult(TypedDict):
    total_countries: int
    added_countries: int
    updated_countries: int
    error_countries: int


@dataclass
class InitCountriesHandler:
    session: MainAsyncSession

    async def execute(self, csv_path: Path | None = None) -> InitCountriesResult:
        map_countries_table()
        Countries = mapping_registry.metadata.tables["countries"]  # type: ignore

        if csv_path is None:
            base = Path(__file__).resolve()
            # Prefer project-root dump/countries.csv
            try:
                csv_candidate = base.parents[5] / "dump" / "countries.csv"
            except IndexError:
                csv_candidate = base
            if csv_candidate.exists():
                csv_path = csv_candidate
            else:
                # Fallback to old location
                csv_path = base.parents[3] / "infrastructure" / "persistence_sqla" / "dump" / "countries.csv"

        if not csv_path.exists():
            raise FileNotFoundError(f"Countries data file not found: {csv_path}")

        total = 0
        added = 0
        updated = 0
        errors = 0

        try:
            with csv_path.open(newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    total += 1
                    try:
                        # Expected CSV columns (subset used):
                        # 0: country_id, 1: name, 2: iso3, 3: iso2
                        country_id = int(row[0])
                        name = str(row[1])
                        iso3 = str(row[2]) if row[2] else None
                        raw_iso2 = (row[3] or "").strip().upper()
                        iso2 = raw_iso2 if len(raw_iso2) == 2 and raw_iso2.isalpha() else None

                        select_stmt: Select = select(Countries.c.id).where(
                            Countries.c.country_id == country_id
                        )
                        existing = (await self.session.execute(select_stmt)).first()

                        if existing:
                            await self.session.execute(
                                Countries.update()
                                .where(Countries.c.country_id == country_id)
                                .values(name=name, iso3=iso3, iso2=iso2)
                            )
                            updated += 1
                        else:
                            await self.session.execute(
                                Countries.insert().values(
                                    country_id=country_id,
                                    name=name,
                                    iso3=iso3,
                                    iso2=iso2,
                                )
                            )
                            added += 1
                    except Exception as e:  # noqa: BLE001
                        log.warning("Error processing country row %s: %s", row[:4], e)
                        errors += 1
                        continue

            await self.session.commit()
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error

        return InitCountriesResult(
            total_countries=total,
            added_countries=added,
            updated_countries=updated,
            error_countries=errors,
        )


