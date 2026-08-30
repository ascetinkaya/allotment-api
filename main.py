from fastapi import FastAPI
from database import engine, Base
from routers import hotels, availability, bookings, admin

Base.metadata.create_all(bind=engine)

import seed_data

app = FastAPI(
    title="AllotmentAPI Project",
    description="""A B2B hotel distribution API for searching availability and managing bookings.

Built by [ascetinkaya](https://github.com/ascetinkaya) — source code available on [GitHub](https://github.com/ascetinkaya/allotment-api).

Use these keys in the `X-API-Key` header to test protected endpoints:

- **Partner A:** `test-key-partner-a`
- **Partner B:** `test-key-partner-b`

Admin key is not publicly available.
""",
    version="1.1"
)

app.include_router(hotels.router, prefix="/hotels", tags=["Hotels(Public access)"])
app.include_router(availability.router, prefix="/availability", tags=["Availability(Public Access)"])
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings(Partner key required)"])
app.include_router(admin.router, prefix="/admin", tags=["Admin(Admin key required)"])

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.1"}