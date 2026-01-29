import pytest
from sqlalchemy import select
from app.user.models import User

@pytest.mark.asyncio
async def test_create_user(db_session):
    user = User(name="Santosh", email="santosh@gmail.com", password="1234", level=1)
    db_session.add(user)
    await db_session.flush()  # flush to generate ID

    stmt = select(User).where(User.email == "santosh@gmail.com")
    result = await db_session.execute(stmt)
    fetched_user = result.scalar_one_or_none()

    assert fetched_user is not None
    assert fetched_user.name == "Santosh"
    assert fetched_user.email == "santosh@gmail.com"
