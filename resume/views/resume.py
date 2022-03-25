from flask import Blueprint, request
from .. import office
from .. import repo
from . import handle, create_blueprint, token_required
from ..encoding.date import parse_date

bp = create_blueprint("resume", __name__)

@bp.route("/<int:id>")
@token_required
@handle()
def index(id:int):
  return office.find_profile(repo.SaRepository(), id)

@bp.route("/", methods=["POST"])
@token_required
@handle(status_code=201)
def create():
  return office.create_profile(
    repo.SaRepository(),
    request.json.get("firstname", ""),
    request.json.get("lastname", ""),
    request.json.get("email", ""),
    request.json.get("phone", ""),
  )

@bp.route("/<int:id>", methods=["DELETE"])
@token_required
@handle(status_code=204)
def delete(id:int):
  pass


@bp.route("/<int:profile_id>/achievements/", methods=["POST"])
@token_required
@handle(status_code=201)
def add_achievement(profile_id):
  return office.add_achievement(
    repo.SaRepository(),
    profile_id,
    request.json.get("name", ''),
    request.json.get("desc", ''),
    request.json.get("web", ''),
  )

@bp.route("/<int:profile_id>/achievements/<int:achieve_id>", methods=["DELETE"])
@token_required
@handle(status_code=204)
def del_achievement(profile_id, achieve_id):
  office.del_achievement(
    repo.SaRepository(),
    profile_id,
    achieve_id,
  )

@bp.route("/<int:profile_id>/educations/", methods=["POST"])
@token_required
@handle(status_code=201)
def add_education(profile_id: int):
  return office.add_education(
    repo.SaRepository(),
    profile_id,
    request.json.get("school", ""),
    request.json.get("degree", ""),
    parse_date(request.json.get("dtstart", "")),
    parse_date(request.json.get("dtend", "")),
  )

@bp.route("/<int:profile_id>/educations/<int:edu_id>", methods=["DELETE"])
@token_required
@handle(status_code=204)
def del_education(profile_id: int, edu_id: int):
  office.del_education(
    repo.SaRepository(),
    profile_id,
    edu_id,
  )

@bp.route("/<int:profile_id>/careers/", methods=["POST"])
@token_required
@handle(status_code=201)
def add_career(profile_id: int):
  return office.add_career(
    repo.SaRepository(),
    profile_id,
    request.json.get("employer", ""),
    request.json.get("role", ""),
    request.json.get("desc", ""),
    parse_date(request.json.get("dtstart", "")),
    parse_date(request.json.get("dtend", "")),
  )

@bp.route("/<int:profile_id>/careers/<int:career_id>", methods=["PUT"])
@token_required
@handle(status_code=200)
def edit_career(profile_id:int, career_id: int):
  return office.edit_career(
    repo.SaRepository(),
    profile_id,
    career_id,
    request.json.get("employer", ""),
    request.json.get("role", ""),
    request.json.get("desc", ""),
    parse_date(request.json.get("dtstart", "")),
    parse_date(request.json.get("dtend", "")),
  )

@bp.route("/<int:profile_id>/careers/<int:career_id>", methods=["DELETE"])
@token_required
@handle(status_code=204)
def del_career(profile_id: int, career_id: int):
  office.del_career(
    repo.SaRepository(),
    profile_id,
    career_id,
  )

@bp.route("/<int:profile_id>/languages/", methods=["POST"])
@token_required
@handle(status_code=201)
def add_lang(profile_id:int):
  return office.add_language(
    repo.SaRepository(),
    profile_id,
    lang=request.json.get("lang", ""),
    desc=request.json.get("desc", ""),
    level=request.json.get("level", ""),
    mother=request.json.get("mother", ""),
  )

@bp.route("/<int:profile_id>/languages/<int:lang_id>", methods=["PUT"])
@token_required
@handle(status_code=200)
def edit_lang(profile_id:int, lang_id:int):
  return office.edit_language(
    repo.SaRepository(),
    profile_id,
    lang_id,
    desc=request.json.get("desc", ""),
    level=request.json.get("level", ""),
    mother=request.json.get("mother", ""),
  )

@bp.route("/<int:profile_id>/languages/<int:lang_id>", methods=["DELETE"])
@token_required
@handle(status_code=204)
def del_lang(profile_id:int, lang_id:int):
  office.del_language(
    repo.SaRepository(),
    profile_id,
    lang_id,
  )

@bp.route("/<int:profile_id>/hardskills/", methods=["POST"])
@token_required
@handle(status_code=201)
def add_hard_skill(profile_id):
  return office.add_hard_skill(
    repo.SaRepository(),
    profile_id,
    request.json.get("category", ""),
    request.json.get("name", ""),
    request.json.get("desc", ""),
    request.json.get("level", ""),
    request.json.get("seniority", ""),
  )

@bp.route("/<int:profile_id>/hardskills/<int:skill_id>", methods=["PUT"])
@token_required
@handle(status_code=200)
def edit_hard_skill(profile_id, skill_id):
  return office.edit_hard_skill(
    repo.SaRepository(),
    profile_id,
    skill_id,
    request.json.get("desc", ""),
    request.json.get("level", ""),
    request.json.get("seniority", ""),
  )

@bp.route("/<int:profile_id>/hardskills/<int:skill_id>", methods=["DELETE"])
@token_required
@handle(status_code=204)
def del_hard_skill(profile_id, skill_id):
  office.del_hard_skill(
    repo.SaRepository(),
    profile_id,
    skill_id,
  )

@bp.route("/<int:profile_id>/softskills/", methods=["POST"])
@token_required
@handle(status_code=201)
def add_soft_skill(profile_id):
  return office.add_soft_skill(
    repo.SaRepository(),
    profile_id,
    request.json.get("name", ""),
  )

@bp.route("/<int:profile_id>/softskills/<int:skill_id>", methods=["DELETE"])
@token_required
@handle(status_code=204)
def del_soft_skill(profile_id, skill_id):
  office.del_soft_skill(
    repo.SaRepository(),
    profile_id,
    skill_id,
  )
