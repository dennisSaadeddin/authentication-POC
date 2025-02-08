import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash

async def create_users():
    async with AsyncSessionLocal() as session:
        users_data = [
            {"username": "john_doe", "password": "password123"},
            {"username": "alice_smith", "password": "securepass456"},
            {"username": "bob_wilson", "password": "pass789!"},
            {"username": "emma_brown", "password": "emma2024"},
            {"username": "mike_jones", "password": "mikepass!"}
        ]
        
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                hashed_password=get_password_hash(user_data["password"])
            )
            session.add(user)
        
        await session.commit()
        print("Users created successfully!")

if __name__ == "__main__":
    asyncio.run(create_users()) 