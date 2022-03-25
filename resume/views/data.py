from .. import office
from . import handle, create_blueprint, token_required
from .. import repo

bp = create_blueprint("data", __name__)

@bp.route("/languages")
@token_required
@handle()
def get_languages():
  return office.get_languages(repo.SaRepository())

@bp.route("/schools")
@token_required
@handle()
def get_schools():
  return office.get_schools(repo.SaRepository())

@bp.route("/softskills")
@token_required
@handle()
def get_soft_skills():
  return office.get_soft_skills(repo.SaRepository())

@bp.route("/hardskills")
@token_required
@handle()
def get_hard_skills():
  return office.get_hard_skills(repo.SaRepository())
