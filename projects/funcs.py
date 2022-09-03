from main.models import Project, ProjectFiles


def get_projects():
    projects_db = Project.objects.order_by("-id")[0:10]
    return projects_db
