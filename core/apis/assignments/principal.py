from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.decorators import authenticate_principal
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema
from core.apis.teachers.schema import TeacherSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@authenticate_principal
def list_principal_assignments(principal):
    """List all submitted and graded assignments for the principal"""
    principal_assignments = Assignment.get_principal_assignments(principal.principal_id)
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)



@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@authenticate_principal
def list_teachers(principal):
    """Returns list of teachers associated with a principal"""
    teachers = Teacher.get_all_teachers(principal.principal_id)
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)



@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@authenticate_principal
def grade_regrade_assignment(principal, incoming_payload):
    """Grade or regrade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.principal_mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=principal
    )

    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)


