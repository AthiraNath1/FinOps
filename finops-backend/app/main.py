import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
sys.dont_write_bytecode = True
# sys.path.append(os.path.abspath("router/advisor"))
sys.path.append(os.path.abspath("router/underutilized_resources"))
# sys.path.append(os.path.abspath("router/networking"))

# from router.advisor import advisor
from router.underutilized_resources import underutilized_resources
from router.networking import networking
from router.untagged_resources import untagged_resources
from router.integration import integration_api
from router.user_details import user_api
from router.orphan_resources import orphaned_api
from router.advisor import advisor_api
from router.authentication import auth_api
app = FastAPI()

# origins = [
#     "https://pheonix-frontend.azurewebsites.net"  # React dev server
# ]

origins = [
    "http://localhost:5173",  # Your frontend running on this port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(advisor.router)
app.include_router(underutilized_resources.router)
app.include_router(networking.router)
app.include_router(untagged_resources.router)
app.include_router(orphaned_api.router)
app.include_router(integration_api.router)
app.include_router(advisor_api.router)
app.include_router(user_api.router)
app.include_router(auth_api.router)


# import pyodbc

# conn_str = (
#     "DRIVER={ODBC Driver 17 for SQL Server};"
#     "SERVER=tcp:demoserver123.database.windows.net,1433;"
#     "DATABASE=demo-database;"
#     "UID=adminuser@demoserver123;"
#     "PWD=MySecurePassword123;"
#     "Encrypt=yes;"
#     "TrustServerCertificate=no;"
#     "Connection Timeout=30;"
# )
# try:
#     conn = pyodbc.connect(conn_str)
#     print("✅ Connection successful!")
# except Exception as e:
#     print("❌ Connection failed:", e)


# import pyodbc

# conn_str = (
#     "DRIVER={ODBC Driver 17 for SQL Server};"
#     "SERVER=tcp:demoserver123.database.windows.net,1433;"
#     "DATABASE=demo-database;"
#     "UID=adminuser;"
#     "PWD=MySecurePassword123;"
#     "Encrypt=yes;"
#     "TrustServerCertificate=no;"
#     "Connection Timeout=30;"
# )

# try:
#     conn = pyodbc.connect(conn_str)
#     print("✅ Connection successful!")
# except Exception as e:
#     print("❌ Connection failed:", e)

