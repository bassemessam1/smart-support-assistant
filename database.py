tickets_db = {}
next_ticket_id = 1


def create_ticket(title: str, description: str, customer_name: str):
    global next_ticket_id
    ticket_id = next_ticket_id
    next_ticket_id += 1
    tickets_db[ticket_id] = {
    "ticket_id": ticket_id,
    "title": title,
    "customer_name": customer_name,
    "description": description,
    "status": "open"
    }
    return tickets_db[ticket_id]


def update_ticket(ticket_id: int, description: str):
    if ticket_id not in tickets_db:
        return {"error": "Ticket not found"}
    tickets_db[ticket_id]["description"] = description
    return tickets_db[ticket_id]


def get_ticket_status(ticket_id: int):
    # if ticket_id not in tickets_db:
    #     return {"error": "Ticket not found"}
    return {"ticket_id": ticket_id, "status": tickets_db[ticket_id]["status"]}