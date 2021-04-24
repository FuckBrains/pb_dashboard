from pb_db_api import models, schemas
from sqlalchemy.orm import Session


def get(
    db: Session,
    req_body: schemas.MarketBalanceGet,
) -> schemas.MarketBalanceOut:
    """Return design market balance model."""
    market: models.DesignMarket = db.query(models.DesignMarket).filter_by(
        name=req_body.name,
    ).first()
    if not market:
        err_msg = ('There is not {} market.').format(req_body.name)
        raise ValueError(err_msg)
    if req_body.start and req_body.end:
        balances = db.query(models.DesignMarketBalance).filter(
            models.DesignMarketBalance.design_market == market,
            models.DesignMarketBalance.create_at >= req_body.start,
            models.DesignMarketBalance.create_at <= req_body.end,
        ).order_by(models.DesignMarketBalance.create_at).all()
    else:
        balances = db.query(models.DesignMarketBalance).filter_by(
            design_market=market
        ).order_by(
            models.DesignMarketBalance.create_at.desc()
        ).limit(1).all()

    out_balance_schema = schemas.MarketBalanceOut(
        name=market.name,
        display_name=market.display_name,
        balances=[],
    )
    for _balance in balances:
        out_balance_schema.balances.append(
            schemas.MarketBalanceData(
                balance=_balance.balance,
                create_at=_balance.create_at,
            )
        )
    return out_balance_schema


def make(
    db: Session,
    req_body: schemas.MarketBalanceMake,
) -> schemas.MarketBalanceOut:
    """Make design market balance model."""
    market = db.query(models.DesignMarket).filter_by(
        name=req_body.name,
    ).first()
    if not market:
        market = models.DesignMarket(
            name=req_body.name,
            display_name=req_body.display_name,
        )
        db.add(market)
    market.display_name = req_body.display_name
    _balance: models.DesignMarketBalance = models.DesignMarketBalance(
        design_market=market,
        balance=req_body.balance
    )
    db.add(_balance)
    db.commit()
    db.refresh(_balance)
    out_balance = schemas.MarketBalanceData(
        balance=_balance.balance,
        create_at=_balance.create_at,
    )
    out_balance_schema = schemas.MarketBalanceOut(
        name=market.name,
        display_name=market.display_name,
        balances=[out_balance],
    )
    return out_balance_schema
