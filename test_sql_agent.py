from app.agents.sql_agent import ask_question

question = "What products were sold in April 2023 and how many units?"
answer = ask_question(question)

print("\n📊 Answer:")
print(answer)
