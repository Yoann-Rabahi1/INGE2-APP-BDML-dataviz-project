from utils.imports import st
from utils.constants import MY_COURSES
from ui.components import afficher_cours_par_matrice


def show_courses() -> None:

    afficher_cours_par_matrice(MY_COURSES)