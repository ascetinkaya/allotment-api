from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Hotel, RoomType, Partner
from schemas import HotelCreate, HotelResponse, HotelUpdate, RoomTypeCreate, RoomTypeResponse, RoomTypeUpdate, PartnerResponse
from auth import get_admin
from typing import List

router = APIRouter()

@router.post("/hotels", response_model=HotelResponse, summary="Create Hotel")
def create_hotel(hotel: HotelCreate, db: Session = Depends(get_db), admin = Depends(get_admin)):
    db_hotel = Hotel(**hotel.model_dump())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

@router.patch("/hotels/{hotel_id}", response_model=HotelResponse, summary="Update Hotel")
def update_hotel(hotel_id: int, hotel: HotelUpdate, db: Session = Depends(get_db), admin = Depends(get_admin)):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found.")
    for key, value in hotel.model_dump(exclude_unset=True).items():
        setattr(db_hotel, key, value)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

@router.post("/rooms", response_model=RoomTypeResponse, summary="Create Room Type")
def create_room(room: RoomTypeCreate, db: Session = Depends(get_db), admin = Depends(get_admin)):
    hotel = db.query(Hotel).filter(Hotel.id == room.hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found.")
    existing = db.query(RoomType).filter(
    RoomType.hotel_id == room.hotel_id,
    RoomType.name == room.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="A room type with this name already exists for this hotel.")
    db_room = RoomType(**room.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.patch("/rooms/{room_id}", response_model=RoomTypeResponse, summary="Update Room Type")
def update_room(room_id: int, room: RoomTypeUpdate, db: Session = Depends(get_db), admin = Depends(get_admin)):
    db_room = db.query(RoomType).filter(RoomType.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room type not found.")
    for key, value in room.model_dump(exclude_unset=True).items():
        setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.get("/partners", response_model=List[PartnerResponse], summary="List Partners")
def list_partners(db: Session = Depends(get_db), admin = Depends(get_admin)):
    return db.query(Partner).all()

@router.post("/partners", response_model=PartnerResponse, summary="Create Partner")
def create_partner(name: str, api_key: str, db: Session = Depends(get_db), admin = Depends(get_admin)):
    existing = db.query(Partner).filter(Partner.api_key == api_key).first()
    if existing:
        raise HTTPException(status_code=409, detail="API key already exists.")
    partner = Partner(name=name, api_key=api_key, is_active=True)
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner

@router.patch("/partners/{partner_id}", response_model=PartnerResponse, summary="Update Partner")
def update_partner(partner_id: int, is_active: bool, db: Session = Depends(get_db), admin = Depends(get_admin)):
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found.")
    partner.is_active = is_active
    db.commit()
    db.refresh(partner)
    return partner