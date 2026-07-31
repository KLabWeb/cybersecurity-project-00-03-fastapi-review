from pydantic import BaseModel

class TrackingCookie(BaseModel):
    session_id: str | None = None
    facebook_tracker_id: str | None = None
    google_tracker_id: str | None = None