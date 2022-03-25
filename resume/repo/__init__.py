from sqlalchemy import (
  and_,
  select,
  delete,
  Table,
  Column,
  Boolean,
  Integer,
  String,
  Date,
  ForeignKey,
  create_engine,
  CheckConstraint,
  UniqueConstraint
)
from sqlalchemy.orm import (
  registry,
  sessionmaker,
  scoped_session,
  relationship
)

from .. import staff

mapreg = registry()

profiles = Table(
    "profiles",
    mapreg.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("phone", String, nullable=False, unique=True),
    Column("email", String, nullable=False, unique=True),
    Column("web", String),
    Column("about", String),
    Column("position", String, nullable=False),
)

educations = Table(
  "educations",
  mapreg.metadata,
  Column("id", Integer, primary_key=True, autoincrement=True),
  Column("school", String, nullable=False),
  Column("degree", String),
  Column("dtstart", Date, nullable=False),
  Column("dtend", Date, nullable=False),
  Column("profile_id", ForeignKey("profiles.id")),
)

careers = Table(
    "careers",
    mapreg.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("dtstart", Date, nullable=False),
    Column("dtend", Date, nullable=True),
    Column("title", String, nullable=False),
    Column("desc", String, nullable=False),
    Column("employer", String, nullable=False),
    Column("profile_id", ForeignKey("profiles.id")),
)

career_items = Table(
    "career_items",
    mapreg.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("dtstart", Date, nullable=False),
    Column("dtend", Date, nullable=True),
    Column("title", String, nullable=False),
    Column("desc", String, nullable=False),
    Column("career_id", ForeignKey("careers.id")),
)

achievements = Table(
    "achievements",
    mapreg.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("desc", String),
    Column("web", String),
    Column("profile_id", ForeignKey("profiles.id")),
)

languages = Table(
    "languages",
    mapreg.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("lang", String),
    Column("mother", Boolean),
    Column("desc", String),
    Column("level", Integer, nullable=False),
    Column("profile_id", ForeignKey("profiles.id")),
    CheckConstraint('level >= 0 and level <= 10', name='max_lang_level'),
    UniqueConstraint('lang', 'profile_id', name='profile_lang'),
)

interests = Table(
    "interests",
    mapreg.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("profile_id", ForeignKey("profiles.id")),
    UniqueConstraint('name', 'profile_id', name='profile_interest'),
)

soft_skills = Table(
    "soft_skills",
    mapreg.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("profile_id", ForeignKey("profiles.id")),
    UniqueConstraint('name', 'profile_id', name='profile_soft'),
)

hard_skills = Table(
    "hard_skills",
    mapreg.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("category", String, nullable=False),
    Column("name", String, nullable=False),
    Column("desc", String),
    Column("level", Integer, nullable=False),
    Column("seniority", Integer, nullable=False, default=0),
    Column("profile_id", ForeignKey("profiles.id")),
    CheckConstraint('level >= 0 and level <= 10', name='max_hard_level'),
    CheckConstraint("seniority >= 0", name="hard_seniority"),
    UniqueConstraint('category', 'name', 'profile_id', name='profile_hard'),
)

session = None

def create_session(uri: str):
    global session

    mapreg.map_imperatively(staff.Education, educations)
    mapreg.map_imperatively(staff.HardSkill, hard_skills)
    mapreg.map_imperatively(staff.SoftSkill, soft_skills)
    mapreg.map_imperatively(staff.Interest, interests)
    mapreg.map_imperatively(staff.Language, languages)
    mapreg.map_imperatively(staff.Achievement, achievements)
    mapreg.map_imperatively(staff.CareerItem, career_items)
    mapreg.map_imperatively(staff.Career, careers, properties={
        "items": relationship(staff.CareerItem)
    })
    mapreg.map_imperatively(staff.Profile, profiles, properties={
        "careers": relationship(staff.Career),
        "languages": relationship(staff.Language),
        "softs": relationship(staff.SoftSkill),
        "interests": relationship(staff.Interest),
        "hards": relationship(staff.HardSkill),
        "achievements": relationship(staff.Achievement),
        "educations": relationship(staff.Education),
    })

    engine = create_engine(uri)
    mapreg.metadata.create_all(engine)

    session = scoped_session(sessionmaker(bind=engine))

def get_session():
    global session
    return session()

class NotFoundException(Exception):
  pass

class CredentialsException(Exception):
  pass

class SaRepository:

  def __init__(self):
    self.sess = get_session()

  def get(self, id):
    p = self.sess.query(staff.Profile).filter_by(id=id).first()
    if p is None:
      raise NotFoundException()
    return p

  def authenticate(self, mail, pwd):
    p = self.sess.query(staff.Profile).filter_by(email=mail).first()
    if p is None:
      raise CredentialsException()
    return p

  def add(self, obj):
    self.sess.add(obj)
    self.sess.commit()
    return obj

  def find(self, kls, profile, id):
    q = self.sess.query(kls).filter(and_(kls.id==id, kls.profile_id==profile)).first()
    if q is None:
      raise NotFoundException()
    return q

  def delete(self, kls, profile, id):
    q = delete(kls).where(kls.id==id, kls.profile_id==profile)
    self.sess.execute(q)
    self.sess.commit()

  def get_hard_skills(self):
    q = select(staff.HardSkill.category, staff.HardSkill.name)
    it = get_session().execute(q).unique()
    return [{'cat': i[0], 'name': i[1]} for i in it]

  def get_soft_skills(self):
    q = select(staff.SoftSkill.name)
    it = get_session().execute(q).unique()
    return [i[0] for i in it]

  def get_schools(self):
    q = select(staff.Education.school)
    it = get_session().execute(q).unique()
    return [i[0] for i in it]

  def get_languages(self):
    q = select(staff.Language.lang)
    it = get_session().execute(q).unique()
    return [i[0] for i in it]
