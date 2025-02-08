import asyncio
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.user import User

async def view_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        print("\nUsers in the database:")
        print("-" * 100)
        print(f"{'ID':<5} {'Username':<15} {'Created At':<25} {'Updated At':<25}")
        print("-" * 100)
        
        for user in users:
            created_at = user.created_at.strftime("%Y-%m-%d %H:%M:%S") if user.created_at else ""
            updated_at = user.updated_at.strftime("%Y-%m-%d %H:%M:%S") if user.updated_at else ""
            print(f"{user.id:<5} {user.username:<15} {created_at:<25} {updated_at:<25}")

if __name__ == "__main__":
    asyncio.run(view_users()) 