import json
import os
import random


class PreguntaTest:
    def __init__(self, pregunta="", opciones=[], solucion="", examen=""):
        self.pregunta = pregunta
        self.opciones = opciones
        self.solucion = solucion
        self.examen = examen

    def __str__(self) -> str:
        return f"""
            Pregunta: {self.pregunta}
            Examen: {self.examen}
            Opciones: {self.opciones}
        """


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    header()


def header():
    print()
    print(" $$$$$$$$\  $$$$$$\   $$$$$$\  $$\      $$\ ")
    print(" $$  _____|$$  __$$\ $$  __$$\ $$$\    $$$ |")
    print(" $$ |      $$ /  \__|$$ /  $$ |$$$$\  $$$$ |")
    print(" $$$$$\    $$ |      $$ |  $$ |$$\$$\$$ $$ |")
    print(" $$  __|   $$ |      $$ |  $$ |$$ \$$$  $$ |")
    print(" $$ |      $$ |  $$\ $$ |  $$ |$$ |\$  /$$ |")
    print(" $$$$$$$$\ \$$$$$$  | $$$$$$  |$$ | \_/ $$ |")
    print(" \________| \______/  \______/ \__|     \__|")
    print()


def menu(func):
    def wrapper(*args, **kwargs):
        answer = -1
        while True:
            clear()
            func(*args)
            answer = input().lower().strip()
            if answer.isnumeric() and int(answer) <= len(kwargs['actions']) and int(answer) > 0:
                break
            print("La opcion introducida no es valida")
            input("Press any key to continue...")
        kwargs['actions'][int(answer) - 1]()
    return wrapper


def load(file="test-ecom.json"):
    examsQuestions, categories = [], set()
    with open(file, "r") as jsonData:
        data = json.load(jsonData)
        for question in data:
            examsQuestions.append(PreguntaTest())
            examsQuestions[-1].__dict__.update(question)
            categories.add(question["examen"])

    return examsQuestions, categories


@menu
def mainMenu(title, options,
             inputText="Selecciona la opcion que desees para continuar:"):
    print(title)
    for index in range(len(options)):
        print(f"    {index + 1}- {options[index]}")
    print(f"    {len(options) + 1}- Salir")
    print(inputText, end=" ")


@menu
def categoriesMenu(options, selectedCategories):
    print("Lista de categorias disponibles: ")
    for index in range(len(options)):
        print(
            f"    [{'x' if options[index] in selectedCategories else ' '}] - {options[index]} ({index + 1})")

    print(f"    {len(options) + 1} - Volver al menu")
    print("Indique la categoria de desea eliminar/agregar:", end=" ")


def toggleCategory(category, selectedCategories, callCategoriesMenu):
    if category in selectedCategories and len(selectedCategories) != 1:
        selectedCategories.remove(category)
    else:
        selectedCategories.add(category)
    callCategoriesMenu(selectedCategories)


def nextIndex(questions, selectedCategories, index, callMainMenu):
    for newIndex in range(index, len(questions)):
        if questions[newIndex].examen in selectedCategories:
            return newIndex
    callMainMenu(selectedCategories)


def nextQuestion(option, solucion, callPlayMenu, index, acertadas, totales):
    totales += 1
    if int(option) == int(solucion):
        print("Respuesta correcta")
        acertadas += 1
    else:
        print(f"La respuesta correcta es la {int(solucion) + 1}")
    input("Press any key to continue...")
    callPlayMenu(index, acertadas, totales)


def main():
    examsQuestions, selectedCategories = load()
    random.shuffle(examsQuestions)
    categories = sorted(list(selectedCategories))
    acertadas, totales = 0, 0

    def callCategoriesMenu(selectedCategories): return categoriesMenu(
        categories,
        selectedCategories,
        actions=[
            lambda category=category: toggleCategory(
                category,
                selectedCategories,
                callCategoriesMenu
            ) for category in categories
        ] + [lambda: callMainMenu(selectedCategories)]
    )

    def callMainMenu(selectedCategories): return mainMenu(
        "Menu principal test ecom:",
        ["Empezar los test", "Elegir contenido"],
        actions=[
            lambda: callPlayMenu(
                nextIndex(examsQuestions, selectedCategories, 0, callMainMenu),
                acertadas, totales),
            lambda: callCategoriesMenu(selectedCategories),
            lambda: exit()
        ])

    def callPlayMenu(index, acertadas, totales): return mainMenu(
        examsQuestions[index].pregunta + f" ({examsQuestions[index].examen})",
        examsQuestions[index].opciones,
        f"Selecciona la opcion correcta ({acertadas} acertadas/{totales} totales):",
        actions=[
            lambda option=option: nextQuestion(
                option,
                examsQuestions[index].solucion,
                callPlayMenu,
                nextIndex(examsQuestions, selectedCategories,
                          index + 1, callMainMenu),
                acertadas,
                totales
            ) for option in range(len(examsQuestions[index].opciones))
        ] + [lambda: callMainMenu(selectedCategories)]
    )

    callMainMenu(selectedCategories)


if __name__ == "__main__":
    main()
