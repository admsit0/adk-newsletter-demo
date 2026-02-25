def get_upcoming_events(month: str) -> str:
    """Consulta la base de datos interna del GDG UAM para obtener fechas de eventos."""
    events_db = {
        "marzo": [
            {"dia": 14, "titulo": "Workshop ADK", "sala": "Lab 4", "speaker": "Tú"},
            {"dia": 21, "titulo": "Pizza & Networking", "sala": "Cafetería", "speaker": "Comunidad"}
        ],
        "abril": [
            {"dia": 11, "titulo": "Google I/O Extended", "sala": "Salón de Actos", "speaker": "Streaming"}
        ]
    }
    return str(events_db.get(month.lower().strip(), f"No hay eventos confirmados para {month}."))
