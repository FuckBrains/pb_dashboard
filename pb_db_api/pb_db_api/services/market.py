from pb_db_api import models, schemas
from sqlalchemy.orm import Session


def get(
    db: Session,
    req_body: schemas.Command,
) -> schemas.Markets:
    """Return design markets names."""
    if req_body.cmd != 'all':
        return schemas.Markets()
    markets = db.query(models.DesignMarket).all()

    out_markets_schema = schemas.Markets(
        names=[],
    )
    for market in markets:
        out_markets_schema.names.append(
            schemas.Market(
                name=market.name,
                display_name=market.display_name,
            )
        )
    return out_markets_schema
