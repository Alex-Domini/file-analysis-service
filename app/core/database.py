from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
DATA_FILE = BASE_DIR / "database.db"

engine = create_async_engine(
    f"sqlite+aiosqlite:///{DATA_FILE}",
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
