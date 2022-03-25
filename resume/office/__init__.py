from sqlalchemy import select, delete

from ..repo import get_session, profiles
from .. import staff
from .errors import AuthenticationException, NotFoundException, InvalidIntervalException

def authenticate(repo, email, passwd):
  return repo.authenticate(email, passwd)

def get_languages(repo):
    return repo.get_languages()

def get_schools(repo):
    return repo.get_schools()

def get_soft_skills(repo):
    return repo.get_soft_skills()

def get_hard_skills(repo):
    return repo.get_hard_skills()

def find_profile(repo, id:int):
  return repo.get(id)

def create_profile(repo, fst:str, lst:str, email:str, phone:str):
  p = staff.Profile(
    id=None,
    web=None,
    first_name=fst,
    last_name=lst,
    email=email,
    phone=phone,
  )
  return repo.add(p)

def add_language(repo, profile, lang: str, desc: str, level: str, mother: bool):
  lg = staff.Language(
    id=None,
    lang=lang,
    mother=mother,
    desc=desc,
    level=level,
  )
  p = repo.get(profile)
  p.languages.append(lg)
  return repo.add(p)

def edit_language(repo, profile, lang, desc: str, level: int, mother: bool):
  lg = repo.find(staff.Language, profile, lang)
  lg.desc = desc or lg.desc
  lg.level = level or lg.level
  if mother is not None:
    lg.mother = mother

  repo.add(lg)
  return repo.get(profile)

def del_language(repo, profile: int, lang: int):
  repo.delete(staff.Language, profile, lang)

def add_education(repo, profile, school, degree, dtstart, dtend):
  if dtend < dtstart:
    raise InvalidIntervalException(dtstart, dtend)

  edu = staff.Education(
    id=None,
    school=school,
    degree=degree,
    dtstart=dtstart,
    dtend=dtend,
  )
  p = repo.get(profile)
  p.educations.append(edu)
  return repo.add(p)

def del_education(repo, profile, education):
  repo.delete(staff.Education, profile, education)

def add_career(repo, profile, employer, role, desc, dtstart, dtend):
  if dtend < dtstart:
    raise InvalidIntervalException(dtstart, dtend)

  cr = staff.Career(
    id=None,
    title=role,
    employer=employer,
    desc=desc,
    dtstart=dtstart,
    dtend=dtend,
  )
  p = repo.get(profile)
  p.careers.append(cr)
  return repo.add(p)

def edit_career(repo, profile, career, employer, role, desc, dtstart, dtend):
  if dtend < dtstart:
    raise InvalidIntervalException(dtstart, dtend)

  cr = repo.find(staff.Career, profile, career)
  cr.employer = employer or cr.employer
  cr.role = role or cr.role
  cr.desc = desc or cr.desc
  cr.dtstart = dtstart
  cr.dtend = dtend
  
  repo.add(cr)
  return repo.get(profile)

def del_career(repo, profile, career):
  repo.delete(staff.Career, profile, career)

def add_achievement(repo, profile, name, desc, web):
  ac = staff.Achievement(
    id=None,
    name=name,
    desc=desc,
    web=web,
  )
  p = repo.get(profile)
  p.achievements.append(ac)
  return repo.add(p)

def del_achievement(repo, profile, achieve):
  repo.delete(staff.Achievement, profile, achieve)

def add_hard_skill(repo, profile, category, name, desc, level, seniority):
  sk = staff.HardSkill(
    id=None,
    category=category,
    name=name,
    desc=desc,
    level=level,
    seniority=seniority,
  )
  p = repo.get(profile)
  p.hards.append(sk)
  return repo.add(p)

def edit_hard_skill(repo, profile, skill, desc, level, seniority):
  sk = repo.find(staff.HardSkill, profile, skill)
  sk.desc = desc or sk.desc
  sk.level = level or sk.level
  sk.seniority = seniority or sk.seniority

  repo.add(sk)
  return repo.get(profile)


def del_hard_skill(repo, profile, skill):
  repo.delete(staff.HardSkill, profile, skill)

def add_soft_skill(repo, profile, name):
  sk = staff.SoftSkill(
    id=None,
    name=name,
  )
  p = repo.get(profile)
  p.softs.append(sk)
  return repo.add(p)

def del_soft_skill(repo, profile, skill):
  repo.delete(staff.SoftSkill, profile, skill)
