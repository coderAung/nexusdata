from typing import Callable, Any

from sqlalchemy.orm import Session


def do_trx(func:Callable[[], Any], session:Session, depth:int, read_only:bool):
    try:
        result = func()
        if depth == 0:
            if read_only:
                session.expunge_all()
                session.rollback()
            else:
                session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise e