
# Lista de secciones principales para la Home (tarjetas)
main_sections = [
                {
                    "name": "Prestaciones",
                    "endpoint": "prestaciones.prestacion_form",
                    "description": "Confeccion de prestaciones y detalles técnicos administrativos para usuarios DBP"
                 },
                {
                    "name": "Logueos",
                    "endpoint": "logs.logs_listar",
                    "description": "Listado de logueos por legajo - referidos a la prestación creada"}
                ]

# Diccionario de secciones secundarios para cada uno los navbars de cada seccion
navbars = {
            "prestaciones" :
                [
                {"label": "Crear",      "endpoint": "prestaciones.prestacion_form"},
                {"label": "Ver Tablas", "endpoint": "logs.logs_listar"}
                ],
            "logs": [{"label": "Logueos",    "endpoint": "logs.logs_listar"}]
}

#def navbar_for(blueprint_name: str):
#    return navbars.get(blueprint_name) or navbars.get("main", [])