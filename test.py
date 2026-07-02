from conversation.logic import handle_message, reset_state

reset_state()

print(handle_message("need assessment"))
print(handle_message("software engineer"))
print(handle_message("python, communication"))
print(handle_message("add leadership"))