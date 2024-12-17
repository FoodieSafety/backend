from sqlalchemy import Column, String, TIMESTAMP, BigInteger, ForeignKey, Enum, Text
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    # Relationship with login_activities table
    login_activities = relationship("LoginActivity", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}', email='{self.email}')>"

class LoginActivity(Base):
    __tablename__ = "login_activities"

    login_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    login_at = Column(TIMESTAMP, nullable=False)
    login_status = Column(Enum("success", "failed", name="login_status_enum"), nullable=False)
    ip_address = Column(String(50))
    device_info = Column(String(255))

    # Relationship with users table
    user = relationship("User", back_populates="login_activities")

class Newsletter(Base):
    __tablename__ = "newsletters"

    newsletter_id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(Enum("food_recall", "expiration_notice", name="newsletter_type_enum"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    # Define relationships
    subscriptions = relationship("Subscription", back_populates="newsletter", cascade="all, delete-orphan")


class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    state = Column(String(100), nullable=False)
    newsletter_id = Column(BigInteger, ForeignKey("newsletters.newsletter_id", ondelete="CASCADE"))
    subscription_type = Column(
        Enum("food_recall", "expiration_notice", name="subscription_type_enum"),
        nullable=False
    )
    subscribed_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    status = Column(
        Enum("active", "unsubscribed", name="subscription_status_enum"),
        default="active", nullable=False
    )

    # Define relationships
    newsletter = relationship("Newsletter", back_populates="subscriptions")