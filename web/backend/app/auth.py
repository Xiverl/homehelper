from authx import AuthXConfig, AuthX


config = AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY="SECRET_KEY",
    JWT_TOKEN_LOCATION=["headers"],
    JWT_HEADER_NAME="Authorization",
    JWT_HEADER_TYPE="Bearer"
)
auth = AuthX(config=config)
