from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Many-to-many relation between organizations and activities
organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id")),
    Column("activity_id", Integer, ForeignKey("activities.id"))
)

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_numbers = Column(String)  # JSON string or comma-separated list
    building_id = Column(Integer, ForeignKey("buildings.id"))

    building = relationship("Building", backref="organizations")
    activities = relationship(
        "Activity",
        secondary=organization_activity,
        backref="organizations"
    )
